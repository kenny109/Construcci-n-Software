from app.models.publication_type_model import PublicationTypeModel
from app.blueprints import create_crud_blueprint

bp = create_crud_blueprint(PublicationTypeModel, 'publication_types')

@bp.route('/<int:id>/publications', methods=['GET'])
def get_type_publications(id):
    pub_type = PublicationTypeModel.get_by_id(id)
    return jsonify([p.to_dict() for p in pub_type.publications])