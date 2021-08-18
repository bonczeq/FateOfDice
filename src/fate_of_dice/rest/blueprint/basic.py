from flask import Blueprint
from flask import jsonify

basic_blueprint = Blueprint('status', __name__)


@basic_blueprint.route('/status', methods=['GET'])
def status_rest():
    return jsonify(data='FateOfDice alive'), 200
