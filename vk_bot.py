import logging
import os

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType, Event
from vk_api.utils import get_random_id
from vk_api.vk_api import VkApiMethod
from dotenv import load_dotenv

from google_dialogflow_api import get_flow_reply
from logs_handler import TelegramLogsHandler

logger = logging.getLogger(__file__)


def reply_with_flow_vk(
    event: Event,
    vk_api: VkApiMethod,
    google_project_id: str,
) -> None:
    user_id = event.user_id
    user_text = event.text

    flow_reply = get_flow_reply(
        google_project_id=google_project_id, session_id=user_id, user_text=user_text
    )

    if not flow_reply.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=flow_reply.fulfillment_text,
            random_id=get_random_id(),
        )


def main():
    load_dotenv()
    vk_token = os.getenv("VK_TOKEN")
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    telegram_admin_chat_id = os.getenv("TELEGRAM_ADMIN_CHAT_ID")
    google_project_id = os.getenv("GOOGLE_PROJECT_ID")

    logging.basicConfig(level=logging.INFO)
    logger.addHandler(
        TelegramLogsHandler(tg_token=telegram_token, chat_id=telegram_admin_chat_id)
    )

    vk_session = vk_api.VkApi(token=vk_token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    logger.info("📗 VK API long polling started successfully")

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            try:
                reply_with_flow_vk(
                    event=event, vk_api=vk, google_project_id=google_project_id
                )
            except Exception:
                logger.exception()


if __name__ == "__main__":
    main()
