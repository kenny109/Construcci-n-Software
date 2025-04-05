from flask import Flask
from flask import Blueprint
from flask import request
from flask import jsonify
from werkzeug.utils import secure_filename
import json
from flask_cors import CORS, cross_origin 

from backend.models.mysql_task_model import TaskModel
model = TaskModel()

task_blueprint = Blueprint('task_blueprint', __name__)

@task_blueprint.route('/task', methods=['PUT'])
@cross_origin()
def create_task():
    content = model.create_task(request.json['task_title'], request.json['task_description'], request.json['user_id'])    
    return jsonify(content)

@task_blueprint.route('/task', methods=['DELETE'])
@cross_origin()
def delete_task():
    return jsonify(model.delete_task(int(request.json['task_id'])))

@task_blueprint.route('/task', methods=['POST'])
@cross_origin()
def task():
    return jsonify(model.get_task(int(request.json['task_id'])))

@task_blueprint.route('/tasks', methods=['POST'])
@cross_origin()
def tasks():
    return jsonify(model.get_tasks())