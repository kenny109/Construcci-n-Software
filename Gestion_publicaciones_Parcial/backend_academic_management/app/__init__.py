from .config import Config
from .extensions import db, migrate, jwt
from .blueprints import register_blueprints
from .swagger import configure_swagger
from flask import Flask
from flask_cors import CORS
from flask_migrate import upgrade
import os

def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:5173",                     # para desarrollo local
            "https://construcci-n-software-ipbd.vercel.app"             # reemplaza con tu dominio real en Vercel
        ]
    }
}, supports_credentials=True)
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
                # Verificar que las variables estén cargadas
                db_uri = app.config['SQLALCHEMY_DATABASE_URI']
                print(f"Database URI: {db_uri[:50]}...")  # Solo mostrar parte para logs
                
                if '127.0.0.1' in db_uri:
                    print("ERROR: Still using localhost database!")
                    print("Available env vars:", list(os.environ.keys()))
                else:
                    upgrade()
                    print("Database migrations applied successfully!")
            except Exception as e:
                print(f"Error applying migrations: {e}")
    
    return app