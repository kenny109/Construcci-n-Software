from flask import Blueprint
from flask import request
from flask import jsonify
from flask_cors import cross_origin

from project.backend.models.autor_model import AutorModel
from project.backend.auth_middleware import token_required

# Usando el modelo de autores
model = AutorModel()

autor_blueprint = Blueprint('autor_blueprint', __name__)

@autor_blueprint.route('/autor', methods=['POST'])
@cross_origin()
@token_required
def create_autor():
    if not request.json:
        return jsonify({'error': 'Datos no proporcionados'}), 400
    
    required_fields = ['nombre', 'apellido']
    for field in required_fields:
        if field not in request.json:
            return jsonify({'error': f'Campo requerido: {field}'}), 400
    
    content = model.create_autor(
        request.json['nombre'],
        request.json['apellido'],
        request.json.get('nacionalidad', None),
        request.json.get('fecha_nacimiento', None)
    )
    
    return jsonify(content)

@autor_blueprint.route('/autor', methods=['PUT'])
@cross_origin()
@token_required
def update_autor():
    if not request.json or 'autor_id' not in request.json:
        return jsonify({'error': 'ID de autor no proporcionado'}), 400
    
    content = model.update_autor(
        request.json['autor_id'],
        request.json.get('nombre'),
        request.json.get('apellido'),
        request.json.get('nacionalidad'),
        request.json.get('fecha_nacimiento')
    )
    
    if 'error' in content:
        return jsonify(content), 404
    
    return jsonify(content)

@autor_blueprint.route('/autor', methods=['DELETE'])
@cross_origin()
@token_required
def delete_autor():
    if not request.json or 'autor_id' not in request.json:
        return jsonify({'error': 'ID de autor no proporcionado'}), 400
    
    result = model.delete_autor(int(request.json['autor_id']))
    
    if 'error' in result:
        return jsonify(result), 404
    
    return jsonify(result)

@autor_blueprint.route('/autor', methods=['GET'])
@cross_origin()
@token_required
def get_autor():
    if not request.json or 'autor_id' not in request.json:
        return jsonify({'error': 'ID de autor no proporcionado'}), 400
    
    result = model.get_autor(int(request.json['autor_id']))
    
    if not result:
        return jsonify({'error': 'Autor no encontrado'}), 404
    
    return jsonify(result)

@autor_blueprint.route('/autores', methods=['GET'])
@cross_origin()
@token_required
def get_autores():
    return jsonify(model.get_autores())



@autor_blueprint.route('/autor/libros', methods=['GET'])
@cross_origin()
@token_required
def get_libros_by_autor():
    autor_id = request.args.get('autor_id')
    if not autor_id:
        return jsonify({'error': 'ID de autor no proporcionado'}), 400

    result = model.get_libros_by_autor(int(autor_id))
    return jsonify(result)
