import os
import random
import logging

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import telegram

from dialog_flow_handlers import detect_intent_texts

vk_token = os.getenv('SUPPORT_VK_TOKEN')

logger = logging.getLogger(__name__)


class LogsToTelegramHandler(logging.Handler):
    """Обработчик логов, который шлет их в телеграм канал."""
    def __init__(self, telegram_token, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.log_bot = telegram.Bot(token=telegram_token)

    def emit(self, record):
        log_entry = self.format(record)
        self.log_bot.send_message(
            chat_id=self.chat_id, text=log_entry,
            disable_web_page_preview=True
        )


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
    notification_telegram_token = os.getenv("NOTIFICATION_TELEGRAM_TOKEN")
    notification_chat_id = os.getenv("NOTIFICATION_TELEGRAM_CHAT_ID")
    logger.setLevel(logging.INFO)
    logger.addHandler(LogsToTelegramHandler(notification_telegram_token, notification_chat_id))

    logger.info('VKontkte support bot started.')

    vk_session = vk_api.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            dialog_flow_answer(event, vk_api)
