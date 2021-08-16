from threading import Thread
from typing import Final

from flask import Flask, request
from waitress import serve

from fate_of_dice.common import DiceException
from fate_of_dice.resources.resource_handler import ResourceHandler
from fate_of_dice.rest.rest_roll_strategy import RestRollStrategy
from fate_of_dice.rest.system.call_fo_cthulhu import blueprint as call_of_cthulhu_blueprint
from fate_of_dice.system import DiceResult

_FATE_OF_DICE_REST_SECTION: Final[str] = 'FATE_OF_DICE_REST'
_FATE_OF_DICE_REST_URL: Final[str] = 'FATE_OF_DICE_REST_URL'
_FATE_OF_DICE_REST_PORT: Final[str] = 'FATE_OF_DICE_REST_PORT'


class _EmptyRestRollStrategy(RestRollStrategy):

    def execute(self, request_dict: dict, dice_result: DiceResult):
        pass

    def on_error(self, request_dict: dict, error: DiceException):
        pass


app = Flask(__name__)


@app.errorhandler(DiceException)
def handle_dice_exception(error: DiceException):
    rest_roll_strategy: RestRollStrategy = app.config[RestRollStrategy.REST_ROLL_STRATEGY_PROPERTY_NAME]
    rest_roll_strategy.on_error(request.get_json(), error)
    return str(error), 400


class RestServer:
    _is_started: bool = False

    def __init__(self, rest_roll_strategy=_EmptyRestRollStrategy()) -> None:
        self.app = app
        self.app.config[RestRollStrategy.REST_ROLL_STRATEGY_PROPERTY_NAME] = rest_roll_strategy
        self._register_blueprint(self.app)

    @staticmethod
    def _register_blueprint(app: Flask) -> None:
        app.register_blueprint(call_of_cthulhu_blueprint)

    def run(self, thread=False) -> None:
        host = ResourceHandler.get_property(_FATE_OF_DICE_REST_URL, section_name=_FATE_OF_DICE_REST_SECTION,
                                            default='0.0.0.0')
        port = ResourceHandler.get_property(_FATE_OF_DICE_REST_PORT, section_name=_FATE_OF_DICE_REST_SECTION,
                                            default=8080)

        if thread and not self._is_started:
            self._is_started = True
            Thread(target=serve, args=(app,), kwargs={'host': host, 'port': port}, daemon=True).start()
        else:
            serve(app, host=host, port=port)


if __name__ == '__main__':
    RestServer().run()
