from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt
from .blueprints import register_blueprints
from .swagger import configure_swagger

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Inicializar JWT
    jwt.init_app(app)
    
    # Registrar blueprints
    register_blueprints(app)
    
    # Configurar Swagger
    configure_swagger(app)
    
    return app