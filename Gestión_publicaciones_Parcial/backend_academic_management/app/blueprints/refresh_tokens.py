from app.models.refresh_token_model import RefreshTokenModel
from app.blueprints import create_crud_blueprint

bp = create_crud_blueprint(RefreshTokenModel, 'refresh_tokens')