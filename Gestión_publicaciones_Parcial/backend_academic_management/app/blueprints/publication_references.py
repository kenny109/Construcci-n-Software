from app.models.publication_reference_model import PublicationReferenceModel
from app.blueprints import create_crud_blueprint

bp = create_crud_blueprint(PublicationReferenceModel, 'publication_references')