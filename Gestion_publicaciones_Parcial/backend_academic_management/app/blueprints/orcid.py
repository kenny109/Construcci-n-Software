import uuid
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.services.orcid_service import OrcidService
from app.models import Publication, PublicationType, Journal, Conference, Country
from app.extensions import db
from datetime import datetime, date
import traceback
import requests

bp = Blueprint('orcid', __name__)

@bp.route('/', methods=['GET'])
@jwt_required()
def get_orcid_info():
    """Punto final para verificar el servicio de ORCID"""
    return jsonify({
        'status': 'active',
        'message': 'Servicio de integración con ORCID disponible'
    })

@bp.route('/sync/<orcid_id>', methods=['POST'])
@jwt_required()
def sync_researcher(orcid_id):
    """Sincroniza datos de un investigador desde ORCID"""
    result = OrcidService.sync_researcher_data(orcid_id)
    return jsonify(result)

@bp.route('/researcher/<orcid_id>', methods=['GET'])
@jwt_required()
def get_researcher(orcid_id):
    """Obtiene información básica de un investigador por su ORCID ID"""
    researcher_info = OrcidService.get_researcher_info(orcid_id)
    
    if not researcher_info:
        return jsonify({
            'success': False,
            'message': 'No se pudo obtener información del investigador'
        }), 404
    
    person = researcher_info.get('person', {})
    name = person.get('name', {})
    
    researcher_data = {
        'orcid_id': orcid_id,
        'first_name': name.get('given-names', {}).get('value', ''),
        'last_name': name.get('family-name', {}).get('value', ''),
        'credit_name': name.get('credit-name', {}).get('value', ''),
        'email': OrcidService._extract_email(person),
        'affiliation': OrcidService._extract_affiliation(person)
    }
    
    return jsonify({
        'success': True,
        'data': researcher_data
    })

@bp.route('/researcher/<orcid_id>/works', methods=['GET'])
@jwt_required()
def get_works(orcid_id):
    """Obtiene las publicaciones de un investigador por su ORCID ID"""
    works = OrcidService.get_researcher_works(orcid_id)
    
    if not works:
        return jsonify({
            'success': False,
            'message': 'No se pudieron obtener las publicaciones del investigador'
        }), 404
    
    simplified_works = []
    for work_group in works:
        work = OrcidService._get_preferred_work(work_group)
        if work:
            external_id = OrcidService._extract_external_id(work)
            
            # Asegurarse de que journal-title no sea None
            journal_info = work.get('journal-title')
            journal = journal_info.get('value', '') if journal_info else ''
            
            simplified_works.append({
                'title': work.get('title', {}).get('title', {}).get('value', 'Sin título'),
                'type': work.get('type'),
                'year': OrcidService._extract_year(work),
                'journal': journal,
                'external_id': external_id,
                'doi': OrcidService._extract_doi(work),
                'url': OrcidService._extract_url(work)
            })
    
    return jsonify({
        'success': True,
        'count': len(simplified_works),
        'data': simplified_works
    })

@bp.route('/publications', methods=['POST'])
@jwt_required()
def create_publication_from_orcid():
    """Crea una publicación en la base de datos a partir de datos de ORCID"""
    try:
        data = request.get_json()
        
        print("=== INICIO CREATE PUBLICATION FROM ORCID ===")
        print(f"Datos recibidos: {data}")
        
        # Verificar campos obligatorios
        if 'title' not in data:
            return jsonify({'error': 'Campo title es obligatorio'}), 400
        
        # Obtener o crear el tipo de publicación
        publication_type_id = _get_or_create_publication_type(data.get('type', 'journal-article'))
        
        # Preparar los datos de la publicación
        publication_data = {
            'title': data.get('title'),
            'publication_type_id': publication_type_id,
            'external_id': data.get('external_id'),
            'doi': data.get('doi'),
            'url': data.get('url'),
            'year': data.get('year'),
            'citation_count': 0
        }
        
        # Manejar el journal si existe
        journal_name = data.get('journal')
        if journal_name:
            journal_id = _get_or_create_journal(journal_name)
            if journal_id:
                publication_data['journal_id'] = journal_id
        
        # Manejar fechas
        if data.get('year'):
            try:
                # Si no hay fecha específica, usar solo el año
                publication_data['publication_date'] = date(data['year'], 1, 1)
            except (ValueError, TypeError):
                pass
        
        # Agregar campos opcionales si existen
        optional_fields = ['abstract', 'pdf_url', 'month', 'day']
        for field in optional_fields:
            if field in data and data[field] is not None:
                publication_data[field] = data[field]
        
        print(f"Datos de publicación preparados: {publication_data}")
        
        # Crear la publicación
        publication = Publication(**publication_data)
        db.session.add(publication)
        db.session.flush()
        
        print(f"Publicación creada con ID: {publication.id}")
        
        db.session.commit()
        
        # Preparar respuesta
        response_data = {
            'id': str(publication.id),
            'title': publication.title,
            'publication_type_id': str(publication.publication_type_id),
            'year': publication.year,
            'journal_id': str(publication.journal_id) if publication.journal_id else None,
            'doi': publication.doi,
            'url': publication.url,
            'external_id': publication.external_id,
            'publication_date': publication.publication_date.isoformat() if publication.publication_date else None
        }
        
        return jsonify({
            'success': True,
            'message': 'Publicación creada exitosamente',
            'data': response_data
        }), 201
        
    except Exception as e:
        print("=== ERROR EN CREATE PUBLICATION FROM ORCID ===")
        print(f"Error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/publications/batch', methods=['POST'])
@jwt_required()
def create_publications_batch():
    """Crea múltiples publicaciones en lote desde datos de ORCID"""
    try:
        data = request.get_json()
        publications_data = data.get('publications', [])
        
        if not publications_data:
            return jsonify({'error': 'No se proporcionaron publicaciones'}), 400
        
        created_publications = []
        errors = []
        
        for idx, pub_data in enumerate(publications_data):
            try:
                # Verificar que tenga título
                if 'title' not in pub_data:
                    errors.append(f"Publicación {idx}: falta título")
                    continue
                
                # Obtener o crear el tipo de publicación
                publication_type_id = _get_or_create_publication_type(pub_data.get('type', 'journal-article'))
                
                # Preparar los datos de la publicación
                publication_data = {
                    'title': pub_data.get('title'),
                    'publication_type_id': publication_type_id,
                    'external_id': pub_data.get('external_id'),
                    'doi': pub_data.get('doi'),
                    'url': pub_data.get('url'),
                    'year': pub_data.get('year'),
                    'citation_count': 0
                }
                
                # Manejar el journal si existe
                journal_name = pub_data.get('journal')
                if journal_name:
                    journal_id = _get_or_create_journal(journal_name)
                    if journal_id:
                        publication_data['journal_id'] = journal_id
                
                # Manejar fechas
                if pub_data.get('year'):
                    try:
                        publication_data['publication_date'] = date(pub_data['year'], 1, 1)
                    except (ValueError, TypeError):
                        pass
                
                # Agregar campos opcionales
                optional_fields = ['abstract', 'pdf_url', 'month', 'day']
                for field in optional_fields:
                    if field in pub_data and pub_data[field] is not None:
                        publication_data[field] = pub_data[field]
                
                # Crear la publicación
                publication = Publication(**publication_data)
                db.session.add(publication)
                db.session.flush()
                
                created_publications.append({
                    'index': idx,
                    'id': str(publication.id),
                    'title': publication.title
                })
                
            except Exception as e:
                errors.append(f"Publicación {idx}: {str(e)}")
                continue
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Se crearon {len(created_publications)} publicaciones',
            'created': created_publications,
            'errors': errors
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Funciones auxiliares
def _get_or_create_publication_type(type_name):
    """Obtiene o crea un tipo de publicación"""
    try:
        # Mapear tipos de ORCID a nombres más legibles
        type_mapping = {
            'journal-article': 'Artículo de revista',
            'conference-paper': 'Artículo de conferencia',
            'book': 'Libro',
            'book-chapter': 'Capítulo de libro',
            'thesis': 'Tesis',
            'report': 'Reporte',
            'working-paper': 'Documento de trabajo',
            'patent': 'Patente',
            'other': 'Otro'
        }
        
        display_name = type_mapping.get(type_name, type_name)
        
        # Buscar si ya existe
        publication_type = PublicationType.query.filter_by(name=display_name).first()
        
        if not publication_type:
            publication_type = PublicationType(
                name=display_name,
                description=f'Tipo de publicación: {display_name}'
            )
            db.session.add(publication_type)
            db.session.flush()
        
        return publication_type.id
        
    except Exception as e:
        print(f"Error creating publication type: {str(e)}")
        return None

def _get_or_create_journal(journal_name):
    """Obtiene o crea un journal"""
    try:
        if not journal_name:
            return None
        
        # Buscar si ya existe
        journal = Journal.query.filter_by(name=journal_name).first()
        
        if not journal:
            # Obtener país por defecto
            country = Country.query.first()  # Usar el primer país disponible
            
            journal = Journal(
                name=journal_name,
                country_id=country.id if country else None,
                quartile="Q4",  # Quartil por defecto
                h_index=0       # H-index por defecto
            )
            db.session.add(journal)
            db.session.flush()
        
        return journal.id
        
    except Exception as e:
        print(f"Error creating journal: {str(e)}")
        return None

def _get_or_create_conference(conference_name, year=None):
    """Obtiene o crea una conferencia"""
    try:
        if not conference_name:
            return None
        
        # Buscar si ya existe
        query = Conference.query.filter_by(name=conference_name)
        if year:
            query = query.filter_by(year=year)
        
        conference = query.first()
        
        if not conference:
            # Obtener país por defecto
            country = Country.query.first()
            
            conference = Conference(
                name=conference_name,
                year=year or datetime.now().year,
                country_id=country.id if country else None,
                description="Importado desde ORCID"
            )
            db.session.add(conference)
            db.session.flush()
        
        return conference.id
        
    except Exception as e:
        print(f"Error creating conference: {str(e)}")
        return None

        
@bp.route('/fetch-from-orcid', methods=['POST'])
@jwt_required()
def fetch_from_orcid():
    """
    Obtiene datos de un autor desde ORCID y lo registra o actualiza en la base de datos.
    """
    data = request.get_json()

    if not data or not data.get('orcid_id'):
        return jsonify({'error': 'Se requiere el ORCID ID'}), 400

    orcid_id = data['orcid_id']

    try:
        headers = {'Accept': 'application/json'}

        # Obtener datos del perfil
        response = requests.get(
            f'https://pub.orcid.org/v3.0/{orcid_id}/person',
            headers=headers
        )

        if response.status_code != 200:
            return jsonify({'error': f'Error al obtener datos de ORCID: {response.text}'}), 400

        profile_data = response.json() or {}

        # Extraer nombre
        name_data = profile_data.get('name') or {}
        given_names = name_data.get('given-names') or {}
        family_name = name_data.get('family-name') or {}

        first_name = given_names.get('value', '')
        last_name = family_name.get('value', '')

        # Extraer email
        emails_data = profile_data.get('emails') or {}
        email_list = emails_data.get('email') or []
        email = None
        if isinstance(email_list, list) and len(email_list) > 0:
            email = email_list[0].get('email')
            if email == '':
                email = None

        # Extraer afiliación
        affiliation = None
        if 'employments' in profile_data:
            affiliation_list = profile_data.get('employments', {}).get('employment-summary', [])
            if affiliation_list:
                affiliation = affiliation_list[0].get('organization', {}).get('name')

        # Verificar si el autor ya existe
        existing_author = Author.query.filter_by(orcid_id=orcid_id).first()

        if existing_author:
            # Actualizar datos
            author = Author.update(
                existing_author.id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                institution=affiliation
            )
            message = 'Autor actualizado correctamente'
        else:
            # Crear nuevo autor
            author = Author.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                institution=affiliation,
                orcid_id=orcid_id
            )
            message = 'Autor creado correctamente'

        return jsonify({
            'success': True,
            'message': message,
            'author': author.to_dict()
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Error al procesar datos de ORCID: {str(e)}'}), 500