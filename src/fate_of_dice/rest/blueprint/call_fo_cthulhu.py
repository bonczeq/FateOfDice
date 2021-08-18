from flask import Blueprint
from flask import request, jsonify, current_app

from fate_of_dice.rest.rest_roll_strategy import RestRollStrategy
from fate_of_dice.system.call_of_cthulhu import SkillCheckArguments, check_skill

call_of_cthulhu_blueprint = Blueprint('callOfCthulhu', __name__)


@call_of_cthulhu_blueprint.route('/callOfCthulhu', methods=['POST'])
def call_of_cthulhu_rest():
    request_dict: dict = request.get_json()
    arguments = SkillCheckArguments().fill_from_directory(request_dict)

    skill_result = check_skill('REST', 'callOfCthulhuRest', arguments)

    rest_roll_strategy: RestRollStrategy = current_app.config[RestRollStrategy.REST_ROLL_STRATEGY_PROPERTY_NAME]
    rest_roll_strategy.execute(request_dict, skill_result)

    return jsonify(data=skill_result.to_directory()), 200
