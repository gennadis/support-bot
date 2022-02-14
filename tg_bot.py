import logging
import os

from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

from flow import get_flow_reply


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(f"Здравствуйте, {user.first_name}!")


def reply_with_flow(update: Update, content: CallbackContext) -> None:
    user_id = update.effective_user.id
    user_text = update.message.text

    reply = get_flow_reply(session_id=user_id, user_text=user_text)
    update.message.reply_text(reply)


def main():
    load_dotenv()
    TG_TOKEN = os.getenv("TELEGRAM_TOKEN")

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    updater = Updater(TG_TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text, reply_with_flow))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
