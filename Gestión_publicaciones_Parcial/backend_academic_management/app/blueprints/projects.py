from app.models.project_model import ProjectModel
from app.blueprints import create_crud_blueprint

bp = create_crud_blueprint(ProjectModel, 'projects')

@bp.route('/<uuid:id>/timeline', methods=['GET'])
def get_project_timeline(id):
    project = ProjectModel.get_by_id(id)
    timeline = {
        'milestones': [m.to_dict() for m in project.milestones],
        'deliverables': [d.to_dict() for d in project.deliverables],
        'acquisitions': [a.to_dict() for a in project.acquisitions]
    }
    return jsonify(timeline)