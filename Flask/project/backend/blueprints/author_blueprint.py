from flask import Flask
from flask import Blueprint
from flask import request
from flask import jsonify
from werkzeug.utils import secure_filename
import json
from flask_cors import CORS, cross_origin

from backend.models.autor_model import AutorModel  # Usando el modelo de autores
model = AutorModel()  # Creando la instancia de AutorModel para trabajar con la base de datos "author_books"

autor_blueprint = Blueprint('autor_blueprint', __name__)

@autor_blueprint.route('/autor', methods=['POST'])
@cross_origin()
def create_autor():
    content = model.create_autor(
        request.json['nombre'], 
        request.json['apellido'], 
        request.json['nacionalidad'], 
        request.json['fecha_nacimiento']
    )
    return jsonify(content)

@autor_blueprint.route('/autor', methods=['PUT'])
@cross_origin()
def update_autor():
    content = model.update_autor(
        request.json['autor_id'], 
        request.json['nombre'], 
        request.json['apellido'], 
        request.json['nacionalidad'], 
        request.json['fecha_nacimiento']
    )
    return jsonify(content)

@autor_blueprint.route('/autor', methods=['DELETE'])
@cross_origin()
def delete_autor():
    return jsonify(model.delete_autor(int(request.json['autor_id'])))

@autor_blueprint.route('/autor', methods=['GET'])
@cross_origin()
def get_autor():
    return jsonify(model.get_autor(int(request.json['autor_id'])))

@autor_blueprint.route('/autores', methods=['GET'])
@cross_origin()
def get_autores():
    return jsonify(model.get_autores())

