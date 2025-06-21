from .config import Config
from .extensions import db, migrate, jwt
from .blueprints import register_blueprints
from .swagger import configure_swagger
from flask import Flask
from flask_cors import CORS
from flask_migrate import upgrade

def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

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
    
    # Ejecutar migraciones automáticamente en producción
    if not app.config.get('FLASK_DEBUG'):
        with app.app_context():
            try:
                upgrade()
                print("Database migrations applied successfully!")
            except Exception as e:
                print(f"Error applying migrations: {e}")
    
    return app