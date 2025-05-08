from app.models.user_model import UserModel
from app.blueprints import create_crud_blueprint
from flask_jwt_extended import create_access_token
from flask import jsonify, request

bp = create_crud_blueprint(UserModel, 'users')

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = UserModel.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid credentials"}), 401
    token = create_access_token(identity=str(user.id))
    return jsonify(access_token=token)

@bp.route('/<uuid:id>/projects', methods=['GET'])
def get_user_projects(id):
    user = UserModel.get_by_id(id)
    return jsonify([p.to_dict() for p in user.projects])