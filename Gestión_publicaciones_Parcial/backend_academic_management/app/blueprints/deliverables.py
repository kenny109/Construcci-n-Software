from app.models.deliverable_model import DeliverableModel
from app.blueprints import create_crud_blueprint

bp = create_crud_blueprint(DeliverableModel, 'deliverables')