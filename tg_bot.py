import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

from google_dialogflow_api import get_flow_reply
from logs_handler import TelegramLogsHandler


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(f"Здравствуйте, {user.first_name}!")


def reply_with_flow(update: Update, content: CallbackContext) -> None:
    user_id = update.effective_user.id
    user_text = update.message.text

    try:
        flow_reply = get_flow_reply(session_id=user_id, user_text=user_text)
    except Exception:
        logger.exception()

    update.message.reply_text(flow_reply.fulfillment_text)


def main():
    load_dotenv()
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    telegram_admin_chat_id = os.getenv("TELEGRAM_ADMIN_CHAT_ID")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("Logger")
    logger.addHandler(
        TelegramLogsHandler(tg_token=telegram_token, chat_id=telegram_admin_chat_id)
    )
    logger.info("📗 Telegram bot started successfully")

    updater = Updater(telegram_token)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text, reply_with_flow))

    updater.start_polling()
    updater.idle()
    logger.info("📗 Telegram API long polling started successfully")


if __name__ == "__main__":
    main()
