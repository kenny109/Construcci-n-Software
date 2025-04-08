from flask import Blueprint
from flask import request
from flask import jsonify
from flask_cors import cross_origin

from project.backend.models.genero_model import GeneroModel
from project.backend.auth_middleware import token_required

model = GeneroModel()

genero_blueprint = Blueprint('genero_blueprint', __name__)

@genero_blueprint.route('/genero', methods=['POST'])
@cross_origin()
@token_required
def create_genero():
    if not request.json or 'nombre' not in request.json:
        return jsonify({'error': 'Nombre de género no proporcionado'}), 400
    
    content = model.create_genero(request.json['nombre'])
    
    if 'error' in content:
        return jsonify(content), 400
    
    return jsonify(content)

@genero_blueprint.route('/genero', methods=['PUT'])
@cross_origin()
@token_required
def update_genero():
    if not request.json or 'genero_id' not in request.json or 'nombre' not in request.json:
        return jsonify({'error': 'Datos incompletos'}), 400
    
    content = model.update_genero(
        request.json['genero_id'],
        request.json['nombre']
    )
    
    if 'error' in content:
        return jsonify(content), 404
    
    return jsonify(content)

@genero_blueprint.route('/genero', methods=['DELETE'])
@cross_origin()
@token_required
def delete_genero():
    if not request.json or 'genero_id' not in request.json:
        return jsonify({'error': 'ID de género no proporcionado'}), 400
    
    result = model.delete_genero(int(request.json['genero_id']))
    
    if 'error' in result:
        return jsonify(result), 404
    
    return jsonify(result)

@genero_blueprint.route('/genero', methods=['GET'])
@cross_origin()
@token_required
def get_genero():
    if not request.json or 'genero_id' not in request.json:
        return jsonify({'error': 'ID de género no proporcionado'}), 400
    
    result = model.get_genero(int(request.json['genero_id']))
    
    if not result:
        return jsonify({'error': 'Género no encontrado'}), 404
    
    return jsonify(result)

@genero_blueprint.route('/generos', methods=['GET'])
@cross_origin()
@token_required
def get_generos():
    return jsonify(model.get_generos())