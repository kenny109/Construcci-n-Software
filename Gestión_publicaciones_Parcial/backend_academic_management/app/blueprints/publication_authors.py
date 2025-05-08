from app.models.publication_author_model import PublicationAuthorModel
from app.blueprints import create_crud_blueprint

bp = create_crud_blueprint(PublicationAuthorModel, 'publication_authors')

@bp.route('/reorder', methods=['PUT'])
def reorder_authors():
    data = request.get_json()
    for item in data['order']:
        pa = PublicationAuthorModel.query.filter_by(
            publication_id=item['publication_id'],
            author_id=item['author_id']
        ).first()
        if pa:
            pa.author_position = item['position']
    db.session.commit()
    return jsonify({"message": "Authors reordered successfully"})