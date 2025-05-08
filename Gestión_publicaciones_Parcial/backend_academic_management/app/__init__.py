from flask import Flask
from .config import Config
from .extensions import db, migrate
from flask_jwt_extended import jwt_required
from flask import jwt 
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.blueprints import register_blueprint
    register_blueprint(app)
    
    return app