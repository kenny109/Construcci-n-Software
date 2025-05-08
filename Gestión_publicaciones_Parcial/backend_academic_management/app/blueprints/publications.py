from app.models.publication_model import PublicationModel
from app.blueprints import create_crud_blueprint

bp = create_crud_blueprint(PublicationModel, 'publications')

@bp.route('/<uuid:id>/authors', methods=['GET'])
def get_publication_authors(id):
    publication = PublicationModel.get_by_id(id)
    return jsonify([{
        'id': str(pa.author.id),
        'name': pa.author.user.name,
        'position': pa.author_position
    } for pa in publication.publication_authors])

@bp.route('/<uuid:id>/references', methods=['GET'])
def get_publication_references(id):
    publication = PublicationModel.get_by_id(id)
    return jsonify([r.to_dict() for r in publication.publication_references])