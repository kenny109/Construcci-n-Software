from flask import Blueprint
from flask import request
from flask import jsonify
from flask_cors import cross_origin

from project.backend.models.libro_model import LibroModel
from project.backend.auth_middleware import token_required

# Cambiado por tu nuevo modelo
model = LibroModel()

libro_blueprint = Blueprint('libro_blueprint', __name__)

@libro_blueprint.route('/libro', methods=['POST'])
@cross_origin()
@token_required
def create_libro():
    if not request.json:
        return jsonify({'error': 'Datos no proporcionados'}), 400
    
    required_fields = ['titulo', 'autores_ids']
    for field in required_fields:
        if field not in request.json:
            return jsonify({'error': f'Campo requerido: {field}'}), 400
    
    content = model.create_libro(
        request.json['titulo'],
        request.json.get('anio_publicacion'),
        request.json['autores_ids'],
        request.json.get('generos_ids', [])
    )
    
    if 'error' in content:
        return jsonify(content), 400
    
    return jsonify(content)

@libro_blueprint.route('/libro', methods=['PUT'])
@cross_origin()
@token_required
def update_libro():
    if not request.json or 'libro_id' not in request.json:
        return jsonify({'error': 'ID de libro no proporcionado'}), 400
    
    content = model.update_libro(
        request.json['libro_id'],
        request.json.get('titulo'),
        request.json.get('anio_publicacion'),
        request.json.get('autores_ids', []),
        request.json.get('generos_ids', [])
    )
    
    if 'error' in content:
        return jsonify(content), 404
    
    return jsonify(content)

@libro_blueprint.route('/libro', methods=['DELETE'])
@cross_origin()
@token_required
def delete_libro():
    if not request.json or 'libro_id' not in request.json:
        return jsonify({'error': 'ID de libro no proporcionado'}), 400
    
    result = model.delete_libro(int(request.json['libro_id']))
    
    if 'error' in result:
        return jsonify(result), 404
    
    return jsonify(result)

@libro_blueprint.route('/libro', methods=['GET'])
@cross_origin()
@token_required
def get_libro():
    if not request.json or 'libro_id' not in request.json:
        return jsonify({'error': 'ID de libro no proporcionado'}), 400
    
    result = model.get_libro(int(request.json['libro_id']))
    
    if not result:
        return jsonify({'error': 'Libro no encontrado'}), 404
    
    return jsonify(result)

@libro_blueprint.route('/libros', methods=['GET'])
@cross_origin()
@token_required
def get_libros():
    return jsonify(model.get_libros())

@libro_blueprint.route('/libro/autores', methods=['GET'])
@cross_origin()
@token_required
def get_autores_by_libro():
    if not request.json or 'libro_id' not in request.json:
        return jsonify({'error': 'ID de libro no proporcionado'}), 400
    
    result = model.get_autores_by_libro(int(request.json['libro_id']))
    return jsonify(result)