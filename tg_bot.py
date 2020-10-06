import os
import logging

import telegram
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler

from dialog_flow_handlers import detect_intent_texts

token = os.getenv('SUPPORT_TELEGRAM_TOKEN')

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


def start(bot, update):
    """Хендлер для обработки команды /start"""
    bot.sendMessage(chat_id=update.message.chat_id, text="Здравствуйте.")


def handle_text(bot, update):
    """Хендлер, обрабатывающий все текстовые запросы."""
    msg = update.message.text
    user_id = update.effective_user.id

    response = detect_intent_texts(user_id, msg, 'ru')
    if not response:
        response = 'Не совсем понимаю о чем ты.'
    update.message.reply_text(response)


if __name__ == "__main__":
    notification_telegram_token = os.getenv("NOTIFICATION_TELEGRAM_TOKEN")
    notification_chat_id = os.getenv("NOTIFICATION_TELEGRAM_CHAT_ID")
    logger.setLevel(logging.INFO)
    logger.addHandler(LogsToTelegramHandler(notification_telegram_token, notification_chat_id))

    logger.info('Telegram support bot started.')

    updater = Updater(token=token)

    start_handler = CommandHandler('start', start)
    text_handler = MessageHandler(Filters.text, handle_text)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(text_handler)
    updater.start_polling()
