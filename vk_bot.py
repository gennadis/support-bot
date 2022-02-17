import logging
import os

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType, Event
from vk_api.utils import get_random_id
from vk_api.vk_api import VkApiMethod
from dotenv import load_dotenv

from flow import get_flow_reply
from tg_bot import TelegramLogsHandler


def reply_with_flow_vk(event: Event, vk_api: VkApiMethod) -> None:
    user_id = event.user_id
    user_text = event.text

    try:
        flow_reply = get_flow_reply(session_id=user_id, user_text=user_text)
    except Exception:
        logger.exception()

    if not flow_reply.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=flow_reply.fulfillment_text,
            random_id=get_random_id(),
        )


if __name__ == "__main__":
    load_dotenv()
    vk_token = os.getenv("VK_TOKEN")
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    telegram_admin_chat_id = os.getenv("TELEGRAM_ADMIN_CHAT_ID")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("Logger")
    logger.addHandler(
        TelegramLogsHandler(tg_token=telegram_token, chat_id=telegram_admin_chat_id)
    )
    logger.info("📗 VK bot started successfully")

    vk_session = vk_api.VkApi(token=vk_token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    logger.info("📗 VK API long polling started successfully")

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            reply_with_flow_vk(event, vk)
