from app.models import PublicationKeywordModel
from app.blueprints import create_crud_blueprint

bp = Blueprint('publication_keywords_bp', __name__, url_prefix='/api/publication_keywords')

@bp.route('/publication/<uuid:pub_id>/keyword/<int:keyword_id>', methods=['POST'])
def add_keyword_to_publication(pub_id, keyword_id):
    from app.models import PublicationModel, KeywordModel
    publication = PublicationModel.get_by_id(pub_id)
    keyword = KeywordModel.get_by_id(keyword_id)
    publication.keywords.append(keyword)
    db.session.commit()
    return jsonify({"message": "Keyword added to publication"}), 201