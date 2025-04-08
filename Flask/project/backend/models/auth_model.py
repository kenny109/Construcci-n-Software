import jwt
import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from project.backend.models.postgres_connection_pool import PostgreSQLPool
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'kenny_y_marycielo')

class AuthModel:
    def __init__(self):
        self.postgres_pool = PostgreSQLPool()
    
    def register_user(self, username, password):
        # Verificar si el usuario ya existe
        params = {'username': username}
        rv = self.postgres_pool.execute("SELECT usuario_id FROM usuarios WHERE username = %(username)s", params)
        if rv:
            return {'error': 'El usuario ya existe'}
        
        # Hash de la contraseña
        hashed_password = generate_password_hash(password)
        
        data = {
            'username': username,
            'password': hashed_password
        }
        
        query = """INSERT INTO usuarios (username, password) 
                  VALUES (%(username)s, %(password)s) 
                  RETURNING usuario_id"""
                  
        usuario_id = self.postgres_pool.execute(query, data, commit=True)
        
        return {
            'usuario_id': usuario_id,
            'username': username,
            'message': 'Usuario registrado con éxito'
        }
    
    def login(self, username, password):
        params = {'username': username}
        rv = self.postgres_pool.execute("""
            SELECT usuario_id, username, password 
            FROM usuarios 
            WHERE username = %(username)s AND activo = TRUE
        """, params)
        
        if not rv:
            return {'error': 'Usuario no encontrado o inactivo'}
        
        usuario_id = rv[0][0]
        username = rv[0][1]
        hashed_password = rv[0][2]
        
        if check_password_hash(hashed_password, password):
            token = jwt.encode({
                'sub': str(usuario_id),  # Convertir a string
                'username': username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, SECRET_KEY, algorithm='HS256')
            
            if isinstance(token, bytes):
                token = token.decode('utf-8')

            return {
                'token': token,
                'message': 'Inicio de sesión exitoso'
            }
        else:
            return {'error': 'Contraseña incorrecta'}

    def verify_token(self, token):
        
        
        # Asegurarse de que el token sea string
        if isinstance(token, bytes):
            token = token.decode('utf-8')
            
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            
            # Verificar que el usuario existe en la base de datos
            params = {'usuario_id': payload['sub']}
            rv = self.postgres_pool.execute("SELECT usuario_id FROM usuarios WHERE usuario_id = %(usuario_id)s AND activo = TRUE", params)
            if not rv:
                print("Usuario no encontrado o inactivo")
                return None
                
            return payload
        except jwt.ExpiredSignatureError:
            print("Token expirado")
            return None
        except jwt.InvalidTokenError as e:
            print(f"Token inválido: {e}")
            return None
        except Exception as e:
            print(f"Error al verificar token: {e}")
            return None
