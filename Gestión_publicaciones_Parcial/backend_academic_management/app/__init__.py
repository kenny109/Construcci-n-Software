from flask import Flask
from .config import Config
from .extensions import db, migrate
from flask_jwt_extended import JWTManager
from .blueprints import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Inicializar JWT
    jwt = JWTManager(app)
    
    # Registrar blueprints
    register_blueprints(app)
    
    return app