import logging

from fate_of_dice.discord_bot import DiscordBot
from fate_of_dice.rest import RestServer
from fate_of_dice.roll_handler import DiscordSendMessage


def main():
    # noinspection PyArgumentList
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[logging.StreamHandler()]
    )
    logging.info("FateOfDice started")

    discord_bot: DiscordBot = DiscordBot()
    rest_server: RestServer = RestServer(DiscordSendMessage(discord_bot))

    logging.info("FateOfDice rest starting")
    rest_server.run(thread=True)
    logging.info("FateOfDice discord bot starting")
    discord_bot.run(thread=False)
    logging.info("FateOfDice exit")


if __name__ == '__main__':
    main()
