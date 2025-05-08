from app.models.journal_model import JournalModel
from app.blueprints import create_crud_blueprint

bp = create_crud_blueprint(JournalModel, 'journals')

@bp.route('/<uuid:id>/publications', methods=['GET'])
def get_journal_publications(id):
    journal = JournalModel.get_by_id(id)
    return jsonify([p.to_dict() for p in journal.publications])