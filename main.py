import os

from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
import dialogflow_v2 as dialogflow

bot_url = 't.me/GameOfVerbsBot'
token = os.getenv('SUPPORT_TELEGRAM_TOKEN')
dialog_project_id = os.getenv('DIALOG_PROJECT_ID')


def detect_intent_texts(project_id, session_id, text, language_code):
    """Отправялем текст сообщения в Doalog Flow и получаем ответ"""

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
        response.query_result.fulfillment_text))

    return response.query_result.fulfillment_text


def start(bot, update):
    """Хендлер для обработки команды /start"""
    bot.sendMessage(chat_id=update.message.chat_id, text="Здравствуйте.")


def handle_text(bot, update):
    """Хендлер, обрабатывающий все текстовые запросы."""
    msg = update.message.text
    user_id = update.effective_user.id

    response = detect_intent_texts(dialog_project_id, user_id, msg, 'ru')
    update.message.reply_text(response)


updater = Updater(token=token)

start_handler = CommandHandler('start', start)
text_handler = MessageHandler(Filters.text, handle_text)
command_handler = MessageHandler(Filters.command, handle_text)

updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(text_handler)
updater.dispatcher.add_handler(command_handler)
updater.start_polling()
