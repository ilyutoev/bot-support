import os
import random
import logging

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from dialog_flow_handlers import detect_intent_texts
from log_handlers import LogsToTelegramHandler

logger = logging.getLogger(__name__)


def dialog_flow_answer(event, vk_api):
    """Получаем ответ на сообщение пользователя через dialogflow и отправляем его."""

    session_id = f'vk-{event.user_id}'
    message = detect_intent_texts(session_id, event.text)
    if message:
        vk_api.messages.send(
            user_id=event.user_id,
            message=message,
            random_id=random.randint(1, 1000)
        )


if __name__ == "__main__":
    notification_telegram_token = os.getenv("NOTIFICATION_TELEGRAM_TOKEN")
    notification_chat_id = os.getenv("NOTIFICATION_TELEGRAM_CHAT_ID")
    logger.setLevel(logging.INFO)
    logger.addHandler(LogsToTelegramHandler(notification_telegram_token, notification_chat_id))

    logger.info('VKontkte support bot started.')

    vk_token = os.getenv('SUPPORT_VK_TOKEN')

    vk_session = vk_api.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            dialog_flow_answer(event, vk_api)
