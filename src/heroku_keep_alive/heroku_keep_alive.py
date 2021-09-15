import logging
import os
import time
from typing import Final

import requests

INTERVAL: Final[int] = 60
HEROKU_KEEP_ALIVE_URL: Final[str] = 'HEROKU_KEEP_ALIVE_URL'


def get_heroku_keep_alive_url() -> str:
    return os.getenv(HEROKU_KEEP_ALIVE_URL)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s][KEEP_ALIVE] %(message)s',
        handlers=[logging.StreamHandler()]
    )

    heroku_address = get_heroku_keep_alive_url()
    logging.info(f'Heroku keep alive - URL: {heroku_address}')
    time.sleep(5)

    while True:
        requests.get(f'{heroku_address}')
        time.sleep(INTERVAL)


if __name__ == '__main__':
    main()
