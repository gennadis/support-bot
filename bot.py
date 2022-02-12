import logging
import os

from dotenv import load_dotenv


def main():
    load_dotenv()
    TG_TOKEN = os.getenv("TELEGRAM_TOKEN")

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


if __name__ == "__main__":
    main()
