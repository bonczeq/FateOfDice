from fate_of_dice.common import DiceException
from fate_of_dice.discord_bot import DiscordBot
from fate_of_dice.rest import RestRollStrategy
from fate_of_dice.system import DiceResult


class DiscordSendMessage(RestRollStrategy):

    def __init__(self, discord_bot: DiscordBot) -> None:
        self.discord_bot = discord_bot

    def execute(self, request_dict: dict, dice_result: DiceResult):
        channel_ids = request_dict.get('channelIds')
        user_name = request_dict.get('userName')

        if not channel_ids:
            raise DiceException('Parameter channelIds is obligatory')
        if not user_name:
            raise DiceException('Parameter userName is obligatory')

        self.discord_bot.send_dice_result(channel_ids, user_name, dice_result)

    def on_error(self, request_dict: dict, error: DiceException):
        channel_ids = request_dict.get('channelIds')

        if not channel_ids:
            raise DiceException('Parameter channelIds is obligatory')

        self.discord_bot.on_error(channel_ids, error)
