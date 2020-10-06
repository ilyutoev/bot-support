import os
import logging

from telegram.ext import Updater, CommandHandler, Filters, MessageHandler

from dialog_flow_handlers import detect_intent_texts
from log_handlers import LogsToTelegramHandler

token = os.getenv('SUPPORT_TELEGRAM_TOKEN')

logger = logging.getLogger(__name__)


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
