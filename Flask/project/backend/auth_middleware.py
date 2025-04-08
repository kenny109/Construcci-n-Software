from functools import wraps
from flask import request, jsonify
from project.backend.models.auth_model import AuthModel

auth_model = AuthModel()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Verificar si el token está en los headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Token no proporcionado'}), 401
        
        # Verificar el token
        current_user = auth_model.verify_token(token)
        if not current_user:
            return jsonify({'message': 'Token inválido o expirado'}), 401
            
        # No pasamos current_user a la función
        return f(*args, **kwargs)
    
    return decorated