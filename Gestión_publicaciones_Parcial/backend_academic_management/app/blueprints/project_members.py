from app.models.project_member_model import ProjectMemberModel
from app.blueprints import create_crud_blueprint

bp = create_crud_blueprint(ProjectMemberModel, 'project_members')