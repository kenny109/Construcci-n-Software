import sys
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from flask_cors import CORS, cross_origin 

from project.backend.blueprints.libro_blueprint import libro_blueprint
from project.backend.blueprints.autor_blueprint import autor_blueprint
from project.backend.blueprints.genero_blueprint import genero_blueprint
from project.backend.blueprints.auth_blueprint import auth_blueprint

app = Flask(__name__)

app.register_blueprint(libro_blueprint)
app.register_blueprint(autor_blueprint)
app.register_blueprint(genero_blueprint)
app.register_blueprint(auth_blueprint)

# Configuración CORS - permite todas las rutas y métodos
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}}, supports_credentials=True)
if __name__ == "__main__":
    app.run(debug=True)