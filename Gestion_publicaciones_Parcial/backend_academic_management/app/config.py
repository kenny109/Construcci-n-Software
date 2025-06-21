import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    # Debug: verificar qué está pasando
    database_url = os.getenv('DATABASE_URL')
    print(f"DEBUG - DATABASE_URL exists: {database_url is not None}")
    print(f"DEBUG - DATABASE_URL value: {database_url[:50] if database_url else 'None'}...")
    
    if database_url:
        print("Using DATABASE_URL from environment")
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        print("Using individual DB variables")
        SQLALCHEMY_DATABASE_URI = (
            f"postgresql://{os.getenv('DB_USER')}:"
            f"{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}:"
            f"{os.getenv('DB_PORT')}/"
            f"{os.getenv('DB_NAME')}"
        )
    
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')