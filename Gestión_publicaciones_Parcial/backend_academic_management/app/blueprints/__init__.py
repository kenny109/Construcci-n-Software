from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.extensions import db

def create_crud_blueprint(model, name):
    """
    Crea automáticamente un Blueprint con endpoints CRUD para un modelo
    
    Args:
        model: Clase del modelo SQLAlchemy
        name: Nombre del recurso (para la ruta URL)
    
    Returns:
        Flask Blueprint con 5 endpoints básicos:
        - POST /api/{name}/
        - GET /api/{name}/
        - GET /api/{name}/<id>
        - PUT /api/{name}/<id>
        - DELETE /api/{name}/<id>
    """
    bp = Blueprint(f'{name}_bp', __name__, url_prefix=f'/api/{name}')

    @bp.route('/', methods=['POST'])
    @jwt_required()
    def create():
        """Crea un nuevo registro"""
        data = request.get_json()
        try:
            instance = model.create(**data)
            return jsonify({
                'message': f'{name.capitalize()} creado exitosamente',
                'data': instance.to_dict()
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @bp.route('/', methods=['GET'])
    @jwt_required()
    def get_all():
        """Obtiene todos los registros (paginado)"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        query = model.query.paginate(page=page, per_page=per_page)
        
        return jsonify({
            'data': [item.to_dict() for item in query.items],
            'total': query.total,
            'pages': query.pages,
            'current_page': page
        })

    @bp.route('/<uuid:id>', methods=['GET'])
    @jwt_required()
    def get_one(id):
        """Obtiene un registro específico por ID"""
        instance = model.get_by_id(id)
        return jsonify(instance.to_dict())

    @bp.route('/<uuid:id>', methods=['PUT'])
    @jwt_required()
    def update(id):
        """Actualiza un registro existente"""
        data = request.get_json()
        try:
            instance = model.update(id, **data)
            return jsonify({
                'message': f'{name.capitalize()} actualizado exitosamente',
                'data': instance.to_dict()
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @bp.route('/<uuid:id>', methods=['DELETE'])
    @jwt_required()
    def delete(id):
        """Elimina un registro (soft delete si está implementado)"""
        try:
            model.delete(id)
            return jsonify({
                'message': f'{name.capitalize()} eliminado exitosamente'
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    return bp

def register_blueprints(app):
    """Registra todos los blueprints en la aplicación Flask"""
    # Importaciones dinámicas para evitar circular imports
    from .countries import bp as countries_bp
    from .keywords import bp as keywords_bp
    from .publication_types import bp as publication_types_bp
    from .journals import bp as journals_bp
    from .conferences import bp as conferences_bp
    from .deliverables import bp as deliverables_bp
    from .milestones import bp as milestones_bp
    from .project_members import bp as project_members_bp
    from .refresh_tokens import bp as refresh_tokens_bp
    from .publication_references import bp as publication_references_bp
    from .publication_keywords import bp as publication_keywords_bp
    from .acquisitions import bp as acquisitions_bp
    from .users import bp as users_bp
    from .authors import bp as authors_bp
    from .publications import bp as publications_bp
    from .projects import bp as projects_bp
    from .publication_authors import bp as publication_authors_bp

    # Lista de todos los blueprints
    all_blueprints = [
        (countries_bp, '/api/countries'),
        (keywords_bp, '/api/keywords'),
        (publication_types_bp, '/api/publication-types'),
        (journals_bp, '/api/journals'),
        (conferences_bp, '/api/conferences'),
        (deliverables_bp, '/api/deliverables'),
        (milestones_bp, '/api/milestones'),
        (project_members_bp, '/api/project-members'),
        (refresh_tokens_bp, '/api/refresh-tokens'),
        (publication_references_bp, '/api/publication-references'),
        (publication_keywords_bp, '/api/publication-keywords'),
        (acquisitions_bp, '/api/acquisitions'),
        (users_bp, '/api/users'),
        (authors_bp, '/api/authors'),
        (publications_bp, '/api/publications'),
        (projects_bp, '/api/projects'),
        (publication_authors_bp, '/api/publication-authors')
    ]

    # Registrar cada blueprint
    for blueprint, url_prefix in all_blueprints:
        app.register_blueprint(blueprint, url_prefix=url_prefix)

    # Registrar ruta de health check
    @app.route('/api/health')
    def health_check():
        return jsonify({'status': 'healthy', 'message': 'API funcionando correctamente'})