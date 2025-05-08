from app.models.conference_model import ConferenceModel
from app.blueprints import create_crud_blueprint

bp = create_crud_blueprint(ConferenceModel, 'conferences')

@bp.route('/<uuid:id>/publications', methods=['GET'])
def get_conference_publications(id):
    conference = ConferenceModel.get_by_id(id)
    return jsonify([p.to_dict() for p in conference.publications])