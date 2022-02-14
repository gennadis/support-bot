import os

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from dotenv import load_dotenv


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=get_random_id(),
    )


def main(token: str):
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:

            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message=event.text,
            )


if __name__ == "__main__":
    load_dotenv()
    vk_token = os.getenv("VK_API_KEY")

    main(token=vk_token)
