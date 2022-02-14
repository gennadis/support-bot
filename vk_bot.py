import os

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType, Event
from vk_api.utils import get_random_id
from vk_api.vk_api import VkApiMethod
from dotenv import load_dotenv

from flow import get_flow_reply


def reply_with_flow_vk(event: Event, vk_api: VkApiMethod) -> None:
    user_id = event.user_id
    user_text = event.text

    reply = get_flow_reply(session_id=user_id, user_text=user_text)

    vk_api.messages.send(
        user_id=event.user_id,
        message=reply,
        random_id=get_random_id(),
    )


def main(token: str):
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            reply_with_flow_vk(event, vk)


if __name__ == "__main__":
    load_dotenv()
    vk_token = os.getenv("VK_API_KEY")

    main(token=vk_token)
