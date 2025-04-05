from flask import Flask
from flask import Blueprint
from flask import request
from flask import jsonify
from werkzeug.utils import secure_filename
import json
from flask_cors import CORS, cross_origin 

from backend.models.libro_model import LibroModel  # Cambiado por tu nuevo modelo
model = LibroModel()

libro_blueprint = Blueprint('libro_blueprint', __name__)

@libro_blueprint.route('/libro', methods=['POST'])
@cross_origin()
def create_libro():
    content = model.create_libro(
        request.json['titulo'],
        request.json['genero'],
        request.json['anio_publicacion'],
        request.json['autor_id']
    )
    return jsonify(content)

@libro_blueprint.route('/libro', methods=['PUT'])
@cross_origin()
def update_libro():
    content = model.update_libro(
        request.json['libro_id'],
        request.json['titulo'],
        request.json['genero'],
        request.json['anio_publicacion'],
        request.json['autor_id']
    )
    return jsonify(content)

@libro_blueprint.route('/libro', methods=['DELETE'])
@cross_origin()
def delete_libro():
    return jsonify(model.delete_libro(int(request.json['libro_id'])))

@libro_blueprint.route('/libro', methods=['GET'])
@cross_origin()
def get_libro():
    return jsonify(model.get_libro(int(request.json['libro_id'])))

@libro_blueprint.route('/libros', methods=['GET'])
@cross_origin()
def get_libros():
    return jsonify(model.get_libros())
