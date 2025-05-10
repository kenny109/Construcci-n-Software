import requests
import os
from dotenv import load_dotenv
from app.extensions import db
from app.models import Author, Publication, PublicationAuthor, Journal, Conference

load_dotenv()

class OrcidService:
    """Servicio para interactuar con la API de ORCID"""
    
    BASE_URL = "https://pub.orcid.org/v3.0"
    HEADERS = {"Accept": "application/json"}
    
    @classmethod
    def get_researcher_info(cls, orcid_id):
        """Obtiene información básica de un investigador por su ORCID ID"""
        url = f"{cls.BASE_URL}/{orcid_id}"
        response = requests.get(url, headers=cls.HEADERS)
        
        if response.status_code != 200:
            return None
            
        return response.json()
        
    @classmethod
    def get_researcher_works(cls, orcid_id):
        """Obtiene las publicaciones de un investigador por su ORCID ID"""
        url = f"{cls.BASE_URL}/{orcid_id}/works"
        response = requests.get(url, headers=cls.HEADERS)
        
        if response.status_code != 200:
            return []
            
        return response.json().get('group', [])
    
    @classmethod
    def sync_researcher_data(cls, orcid_id):
        """Sincroniza datos de un investigador desde ORCID a la base de datos local"""
        # Obtenemos info básica del investigador
        researcher_info = cls.get_researcher_info(orcid_id)
        if not researcher_info:
            return {"success": False, "message": "No se pudo obtener información del investigador"}
        
        # Extraemos los datos personales
        person = researcher_info.get('person', {})
        name = person.get('name', {})
        first_name = name.get('given-names', {}).get('value', '')
        last_name = name.get('family-name', {}).get('value', '')
        
        # Verificamos si el autor ya existe en nuestra base de datos
        author = Author.query.filter_by(orcid_id=orcid_id).first()
        
        if not author:
            # Creamos un nuevo autor
            author = Author(
                first_name=first_name,
                last_name=last_name,
                orcid_id=orcid_id,
                email=cls._extract_email(person),
                affiliation=cls._extract_affiliation(person)
            )
            db.session.add(author)
            db.session.commit()
        
        # Obtenemos las publicaciones del investigador
        works = cls.get_researcher_works(orcid_id)
        publications_added = 0
        
        for work_group in works:
            # Cada grupo puede tener varias versiones de la misma publicación
            work = cls._get_preferred_work(work_group)
            if not work:
                continue
                
            # Verificamos si la publicación ya existe
            pub_external_id = cls._extract_external_id(work)
            if not pub_external_id:
                continue
                
            existing_pub = Publication.query.filter_by(external_id=pub_external_id).first()
            if existing_pub:
                # Si ya existe, solo nos aseguramos que el autor esté vinculado
                cls._ensure_author_linked(existing_pub.id, author.id)
                continue
            
            # Creamos la publicación
            publication = cls._create_publication_from_orcid(work, pub_external_id)
            if publication:
                # Vinculamos el autor con la publicación
                cls._ensure_author_linked(publication.id, author.id)
                publications_added += 1
        
        db.session.commit()
        return {
            "success": True,
            "message": f"Datos sincronizados correctamente. {publications_added} publicaciones agregadas.",
            "author": {
                "id": author.id,
                "name": f"{author.first_name} {author.last_name}",
                "orcid_id": author.orcid_id
            }
        }
    
    @staticmethod
    def _extract_email(person):
        """Extrae el email de los datos de persona de ORCID"""
        emails = person.get('emails', {}).get('email', [])
        if emails and len(emails) > 0:
            return emails[0].get('email', '')
        return ''
    
    @staticmethod
    def _extract_affiliation(person):
        """Extrae la afiliación de los datos de persona de ORCID"""
        affiliations = person.get('employments', {}).get('employment-summary', [])
        if affiliations and len(affiliations) > 0:
            org = affiliations[0].get('organization', {})
            return org.get('name', '')
        return ''
    
    @staticmethod
    def _get_preferred_work(work_group):
        """Obtiene la versión preferida de una publicación del grupo de trabajos"""
        if not work_group.get('work-summary'):
            return None
            
        works = work_group.get('work-summary', [])
        if not works:
            return None
            
        # Preferimos la versión con más detalles
        return max(works, key=lambda w: len(str(w)))
    
    @staticmethod
    def _extract_external_id(work):
        """Extrae un identificador externo único para la publicación"""
        if not work:
            return None
            
        external_ids = work.get('external-ids', {}).get('external-id', [])
        
        # Preferimos el DOI como identificador
        for ext_id in external_ids:
            if ext_id.get('external-id-type') == 'doi':
                return f"doi:{ext_id.get('external-id-value', '')}"
        
        # Si no hay DOI, usamos cualquier otro identificador disponible
        if external_ids and len(external_ids) > 0:
            id_type = external_ids[0].get('external-id-type', '')
            id_value = external_ids[0].get('external-id-value', '')
            if id_type and id_value:
                return f"{id_type}:{id_value}"
        
        # Si no hay identificadores, usamos el put-code de ORCID
        return f"orcid_work:{work.get('put-code', '')}"
    
    @classmethod
    def _create_publication_from_orcid(cls, work, external_id):
        """Crea una publicación en nuestra base de datos a partir de los datos de ORCID"""
        try:
            # Extraemos los datos básicos de la publicación
            title = work.get('title', {}).get('title', {}).get('value', 'Sin título')
            journal_title = ''
            
            # Determinamos si es una conferencia o un journal
            publication_type_id = 1  # Por defecto, asumimos artículo de journal
            journal_id = None
            conference_id = None
            
            # Extraemos datos de la fuente (journal o conferencia)
            source = work.get('journal-title', {}).get('value', '')
            if source:
                journal_title = source
                # Buscamos si ya existe el journal
                journal = Journal.query.filter_by(name=journal_title).first()
                if not journal:
                    # Creamos un nuevo journal con datos básicos
                    journal = Journal(
                        name=journal_title,
                        country_id=1,  # País por defecto
                        quartile=4,    # Quartil por defecto
                        h_index=0      # H-index por defecto
                    )
                    db.session.add(journal)
                    db.session.flush()
                
                journal_id = journal.id
            else:
                # Si no hay journal, asumimos que es una conferencia
                publication_type_id = 2  # Conferencia
                
                # Buscamos si ya existe la conferencia
                # Nota: Acá falta información para crear una conferencia completa
                # Por ahora creamos con datos mínimos
                conference = Conference(
                    name="Conferencia de " + title[:50],
                    year=cls._extract_year(work),
                    country_id=1,  # País por defecto
                    description="Importado desde ORCID"
                )
                db.session.add(conference)
                db.session.flush()
                conference_id = conference.id
            
            # Creamos la publicación
            publication = Publication(
                title=title,
                abstract=work.get('short-description', ''),
                year=cls._extract_year(work),
                month=cls._extract_month(work),
                day=cls._extract_day(work),
                publication_type_id=publication_type_id,
                journal_id=journal_id,
                conference_id=conference_id,
                external_id=external_id,
                doi=cls._extract_doi(work),
                url=cls._extract_url(work)
            )
            
            db.session.add(publication)
            db.session.flush()
            return publication
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear publicación: {str(e)}")
            return None
    
    @staticmethod
    def _ensure_author_linked(publication_id, author_id):
        """Asegura que el autor esté vinculado a la publicación"""
        # Verificamos si el vínculo ya existe
        pub_author = PublicationAuthor.query.filter_by(
            publication_id=publication_id,
            author_id=author_id
        ).first()
        
        if not pub_author:
            # Creamos el vínculo
            pub_author = PublicationAuthor(
                publication_id=publication_id,
                author_id=author_id,
                is_corresponding=False  # Por defecto, no es autor correspondiente
            )
            db.session.add(pub_author)
    
    @staticmethod
    def _extract_year(work):
        """Extrae el año de publicación"""
        publication_date = work.get('publication-date', {})
        year = publication_date.get('year', {}).get('value')
        return int(year) if year else None
    
    @staticmethod
    def _extract_month(work):
        """Extrae el mes de publicación"""
        publication_date = work.get('publication-date', {})
        month = publication_date.get('month', {}).get('value')
        return int(month) if month else None
    
    @staticmethod
    def _extract_day(work):
        """Extrae el día de publicación"""
        publication_date = work.get('publication-date', {})
        day = publication_date.get('day', {}).get('value')
        return int(day) if day else None
    
    @staticmethod
    def _extract_doi(work):
        """Extrae el DOI de la publicación"""
        external_ids = work.get('external-ids', {}).get('external-id', [])
        for ext_id in external_ids:
            if ext_id.get('external-id-type') == 'doi':
                return ext_id.get('external-id-value', '')
        return None
    
    @staticmethod
    def _extract_url(work):
        """Extrae la URL de la publicación"""
        external_ids = work.get('external-ids', {}).get('external-id', [])
        for ext_id in external_ids:
            if ext_id.get('external-id-type') == 'url':
                return ext_id.get('external-id-value', '')
        return None