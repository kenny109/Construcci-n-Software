import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from flask_cors import CORS, cross_origin 

from project.backend.blueprints.libro_blueprint import libro_blueprint
from project.backend.blueprints.author_blueprint import autor_blueprint

app = Flask(__name__)

app.register_blueprint(libro_blueprint)
app.register_blueprint(autor_blueprint)

cors = CORS(app)

if __name__ == "__main__":
    app.run(debug=True)