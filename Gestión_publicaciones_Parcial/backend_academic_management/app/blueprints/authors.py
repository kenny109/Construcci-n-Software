from app.models.author_model import AuthorModel
from app.blueprints import create_crud_blueprint

bp = create_crud_blueprint(AuthorModel, 'authors')

@bp.route('/<uuid:id>/publications', methods=['GET'])
def get_author_publications(id):
    author = AuthorModel.get_by_id(id)
    return jsonify([{
        'id': str(pa.publication.id),
        'title': pa.publication.title,
        'author_position': pa.author_position
    } for pa in author.publication_authors])