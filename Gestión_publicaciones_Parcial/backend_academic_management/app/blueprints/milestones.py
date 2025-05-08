from app.models.milestone_model import MilestoneModel
from app.blueprints import create_crud_blueprint

bp = create_crud_blueprint(MilestoneModel, 'milestones')

@bp.route('/<uuid:id>/deliverables', methods=['GET'])
def get_milestone_deliverables(id):
    milestone = MilestoneModel.get_by_id(id)
    return jsonify([d.to_dict() for d in milestone.deliverables])