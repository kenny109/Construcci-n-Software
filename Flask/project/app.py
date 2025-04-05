from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from flask_cors import CORS, cross_origin 

from backend.blueprints.task_blueprint import task_blueprint
from backend.blueprints.user_blueprint import user_blueprint

app = Flask(__name__)

app.register_blueprint(task_blueprint)
app.register_blueprint(user_blueprint)

cors = CORS(app)

if __name__ == "__main__":
    app.run(debug=True)