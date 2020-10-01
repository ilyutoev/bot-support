import os
import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from dialog_flow_handlers import detect_intent_texts

vk_token = os.getenv('SUPPORT_VK_TOKEN')


def dialog_flow_answer(event, vk_api):
    """Получаем ответ на сообщение пользователя через dialogflow и отправляем его."""

    message = detect_intent_texts(event.user_id, event.text)
    if message:
        vk_api.messages.send(
            user_id=event.user_id,
            message=message,
            random_id=random.randint(1, 1000)
        )


if __name__ == "__main__":
    vk_session = vk_api.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            dialog_flow_answer(event, vk_api)
