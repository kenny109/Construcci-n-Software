from app.models.keyword_model import KeywordModel
from app.blueprints import create_crud_blueprint

bp = create_crud_blueprint(KeywordModel, 'keywords')