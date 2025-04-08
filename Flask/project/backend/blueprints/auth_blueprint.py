from flask import Blueprint
from flask import request
from flask import jsonify
from flask_cors import cross_origin

from project.backend.models.auth_model import AuthModel

auth_model = AuthModel()
auth_blueprint = Blueprint('auth_blueprint', __name__)

@auth_blueprint.route('/register', methods=['POST'])
@cross_origin()
def register():
    if not request.json or not 'username' in request.json or not 'password' in request.json:
        return jsonify({'message': 'Datos incompletos'}), 400
    
    return jsonify(auth_model.register_user(
        request.json['username'],
        request.json['password']
    ))

@auth_blueprint.route('/login', methods=['POST'])
@cross_origin()
def login():
    if not request.json or not 'username' in request.json or not 'password' in request.json:
        return jsonify({'message': 'Datos incompletos'}), 400
    
    result = auth_model.login(
        request.json['username'],
        request.json['password']
    )
    
    if 'error' in result:
        return jsonify(result), 401
    
    return jsonify(result)