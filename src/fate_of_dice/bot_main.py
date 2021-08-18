import logging

from fate_of_dice.discord_bot import DiscordBot


def main():
    # noinspection PyArgumentList
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[logging.StreamHandler()]
    )
    logging.info("FateOfDice started")

    discord_bot: DiscordBot = DiscordBot().register_commands()

    logging.info("FateOfDice discord bot starting")
    discord_bot.run(thread=False)
    logging.info("FateOfDice exit")


if __name__ == '__main__':
    main()
