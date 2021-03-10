import logging

from fate_of_dice.discord_bot import run_bot


def main():
    # noinspection PyArgumentList
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[logging.StreamHandler()]
    )

    logging.info("FateOfDice started")
    run_bot()
    logging.info("FateOfDice exit")


if __name__ == '__main__':
    main()
