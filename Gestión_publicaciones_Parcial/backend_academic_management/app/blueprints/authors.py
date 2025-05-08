from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.models import Author, PublicationAuthor, Publication
from app.extensions import db
import requests
import json

bp = Blueprint('authors', __name__)

@bp.route('/', methods=['POST'])
@jwt_required()
def create_author():
    data = request.get_json()
    
    # Verificar campos obligatorios
    required_fields = ['first_name', 'last_name']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo {field} es obligatorio'}), 400
    
    try:
        author = Author.create(**data)
        return jsonify({
            'message': 'Autor creado exitosamente',
            'data': author.to_dict()
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/', methods=['GET'])
@jwt_required()
def get_authors():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Filtro de búsqueda por nombre
    query = Author.query.filter_by(is_active=True)
    
    if request.args.get('search'):
        search_term = f"%{request.args.get('search')}%"
        query = query.filter(
            (Author.first_name.ilike(search_term)) | 
            (Author.last_name.ilike(search_term))
        )
    
    # Ordenar
    sort_by = request.args.get('sort_by', 'last_name')
    sort_dir = request.args.get('sort_dir', 'asc')
    
    if hasattr(Author, sort_by):
        order_column = getattr(Author, sort_by)
        if sort_dir.lower() == 'desc':
            query = query.order_by(order_column.desc())
        else:
            query = query.order_by(order_column.asc())
    
    # Paginar
    paginated_query = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'data': [item.to_dict() for item in paginated_query.items],
        'total': paginated_query.total,
        'pages': paginated_query.pages,
        'current_page': page
    })

@bp.route('/<uuid:id>', methods=['GET'])
@jwt_required()
def get_author(id):
    try:
        author = Author.get_by_id(id)
        author_data = author.to_dict()
        
        # Agregar publicaciones del autor
        publications = []
        author_publications = PublicationAuthor.query.filter_by(author_id=id).all()
        
        for pub_author in author_publications:
            publication = Publication.query.filter_by(id=pub_author.publication_id, is_active=True).first()
            if publication:
                publications.append({
                    'id': str(publication.id),
                    'title': publication.title,
                    'publication_date': publication.publication_date.isoformat() if publication.publication_date else None,
                    'doi': publication.doi,
                    'is_corresponding': pub_author.is_corresponding,
                    'author_order': pub_author.author_order
                })
        
        author_data['publications'] = publications
        
        return jsonify(author_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@bp.route('/<uuid:id>', methods=['PUT'])
@jwt_required()
def update_author(id):
    data = request.get_json()
    
    try:
        author = Author.update(id, **data)
        return jsonify({
            'message': 'Autor actualizado exitosamente',
            'data': author.to_dict()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<uuid:id>', methods=['DELETE'])
@jwt_required()
def delete_author(id):
    try:
        Author.delete(id)
        return jsonify({
            'message': 'Autor eliminado exitosamente'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/fetch-from-orcid', methods=['POST'])
@jwt_required()
def fetch_from_orcid():
    data = request.get_json()
    
    if not data.get('orcid_id'):
        return jsonify({'error': 'Se requiere el ORCID ID'}), 400
    
    orcid_id = data['orcid_id']
    
    try:
        # Llamada a la API pública de ORCID
        headers = {
            'Accept': 'application/json'
        }
        
        # Obtener datos del perfil
        response = requests.get(
            f'https://pub.orcid.org/v3.0/{orcid_id}/person',
            headers=headers
        )
        
        if response.status_code != 200:
            return jsonify({'error': f'Error al obtener datos de ORCID: {response.text}'}), 400
        
        profile_data = response.json()
        
        # Obtener datos de las publicaciones
        works_response = requests.get(
            f'https://pub.orcid.org/v3.0/{orcid_id}/works',
            headers=headers
        )
        
        if works_response.status_code != 200:
            return jsonify({'error': f'Error al obtener publicaciones de ORCID: {works_response.text}'}), 400
        
        works_data = works_response.json()
        
        # Extraer información relevante del perfil
        first_name = profile_data.get('name', {}).get('given-names', {}).get('value', '')
        last_name = profile_data.get('name', {}).get('family-name', {}).get('value', '')
        emails = profile_data.get('emails', {}).get('email', [])
        email = emails[0].get('email') if emails else None
        
        # Verificar si el autor ya existe
        existing_author = Author.query.filter_by(orcid_id=orcid_id).first()
        
        if existing_author:
            # Actualizar datos del autor existente
            author = Author.update(
                existing_author.id,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
        else:
            # Crear nuevo autor
            author = Author.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                orcid_id=orcid_id
            )
        
        # Procesar publicaciones (works)
        publications_summary = []
        
        for work in works_data.get('group', []):
            # Obtener el primer work-summary (normalmente el más completo)
            if work.get('work-summary'):
                summary = work['work-summary'][0]
                pub_data = {
                    'title': summary.get('title', {}).get('title', {}).get('value', 'Sin título'),
                    'type': summary.get('type', ''),
                    'publication_date': None,
                    'journal': None,
                    'doi': None
                }
                
                # Extraer fecha
                if summary.get('publication-date'):
                    year = summary['publication-date'].get('year', {}).get('value')
                    month = summary['publication-date'].get('month', {}).get('value', '01')
                    day = summary['publication-date'].get('day', {}).get('value', '01')
                    if year:
                        pub_data['publication_date'] = f"{year}-{month}-{day}"
                
                # Extraer DOI si está disponible
                if summary.get('external-ids', {}).get('external-id'):
                    for ext_id in summary['external-ids']['external-id']:
                        if ext_id.get('external-id-type') == 'doi':
                            pub_data['doi'] = ext_id.get('external-id-value')
                
                # Extraer fuente (journal)
                if summary.get('journal-title'):
                    pub_data['journal'] = summary['journal-title'].get('value')
                
                publications_summary.append(pub_data)
        
        return jsonify({
            'message': 'Datos obtenidos exitosamente de ORCID',
            'author': author.to_dict(),
            'publications': publications_summary
        })
        
    except Exception as e:
        return jsonify({'error': f'Error al procesar datos de ORCID: {str(e)}'}), 500