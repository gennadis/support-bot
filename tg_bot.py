import logging
import os

from dotenv import load_dotenv
import telegram
from telegram import Update, ForceReply
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

from flow import get_flow_reply


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_token: str, chat_id: int):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = telegram.Bot(token=tg_token)

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


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


def main(token: str):
    updater = Updater(token)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text, reply_with_flow))

    updater.start_polling()
    updater.idle()
    logger.info("📗 Telegram API long polling started successfully")


if __name__ == "__main__":
    load_dotenv()
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    telegram_admin_chat_id = os.getenv("TELEGRAM_ADMIN_CHAT_ID")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("Logger")
    logger = TelegramLogsHandler(
        tg_token=telegram_token, chat_id=telegram_admin_chat_id
    )
    logger.info("📗 Telegram bot started successfully")

    main(token=telegram_token)
