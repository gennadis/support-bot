import logging

import telegram


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_token: str, chat_id: int):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = telegram.Bot(token=tg_token)

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)
