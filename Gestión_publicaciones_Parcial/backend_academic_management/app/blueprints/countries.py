from app.models.country_model import CountryModel
from app.blueprints import create_crud_blueprint
from flask_jwt_extended import jwt_required

bp = create_crud_blueprint(CountryModel, 'countries')

@bp.route('/<int:id>/authors', methods=['GET'])
@jwt_required()
def get_country_authors(id):
    country = CountryModel.get_by_id(id)
    return jsonify([a.to_dict() for a in country.authors])

@bp.route('/<int:id>/journals', methods=['GET'])
@jwt_required()
def get_country_journals(id):
    country = CountryModel.get_by_id(id)
    return jsonify([j.to_dict() for j in country.journals])