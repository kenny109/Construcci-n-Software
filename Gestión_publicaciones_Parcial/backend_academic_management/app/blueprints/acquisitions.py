from app.models.acquisition_model import AcquisitionModel
from app.blueprints import create_crud_blueprint

bp = create_crud_blueprint(AcquisitionModel, 'acquisitions')