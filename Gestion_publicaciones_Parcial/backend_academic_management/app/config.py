import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


class Config:
    # Leer si está en Railway (true o false)
    IS_RAILWAY = os.getenv('IS_RAILWAY', 'false').lower() == 'true'

    # Obtener la URL de la base de datos según el entorno
    if IS_RAILWAY:
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
        print("⚙️ Usando DATABASE_URL (Railway)")
    else:
        SQLALCHEMY_DATABASE_URI = os.getenv('PUBLIC_DATABASE_URL')
        print("⚙️ Usando PUBLIC_DATABASE_URL (Local)")

    print(f"🔍 SQLALCHEMY_DATABASE_URI: {SQLALCHEMY_DATABASE_URI[:60]}...")

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'false').lower() in ('true', '1', 't')
