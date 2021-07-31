from flask import Flask, Blueprint, jsonify
from flask_restplus import Api
from ma import ma
from db import db

from resources.tag import Tag, tag_ns
from resources.assignment import Assignment, Assignments, assignments_ns, assignment_ns
from marshmallow import ValidationError

app = Flask(__name__)
bluePrint = Blueprint('api', __name__, url_prefix='/api')
api = Api(bluePrint, doc='/doc', title='Assignment Management Service')
app.register_blueprint(bluePrint)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api.add_namespace(assignments_ns)
api.add_namespace(assignment_ns)
api.add_namespace(tag_ns)


@app.before_first_request
def create_tables():
    db.create_all()


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400


assignment_ns.add_resource(Assignment, '/<int:id>')
assignments_ns.add_resource(Assignments, "")
tag_ns.add_resource(Tag, '/<string:name>')
# tag_ns.add_resource(Tag, "")

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True,host='0.0.0.0')
