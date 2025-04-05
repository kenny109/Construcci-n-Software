from flask import Flask
from flask import Blueprint
from flask import request
from flask import jsonify
from werkzeug.utils import secure_filename
import json
from flask_cors import CORS, cross_origin 

from backend.models.mysql_user_model import UserModel
model = UserModel()


user_blueprint = Blueprint('user_blueprint', __name__)


@user_blueprint.route('/user', methods=['PUT'])
@cross_origin()
def create_user():
    content = model.create_user(request.json['user_name'], request.json['user_lastname'], request.json['user_email'])    
    return jsonify(content)

@user_blueprint.route('/user', methods=['PATCH'])
@cross_origin()
def update_user():
    content = model.update_user(request.json['user_id'], request.json['user_name'], request.json['user_lastname'], request.json['user_email'])    
    return jsonify(content)

@user_blueprint.route('/user', methods=['DELETE'])
@cross_origin()
def delete_task():
    return jsonify(model.delete_user(int(request.json['user_id'])))

@user_blueprint.route('/user', methods=['POST'])
@cross_origin()
def task():
    return jsonify(model.get_user(int(request.json['user_id'])))

@user_blueprint.route('/users', methods=['POST'])
@cross_origin()
def tasks():
    return jsonify(model.get_users())