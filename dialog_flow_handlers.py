import os

import dialogflow_v2 as dialogflow

dialog_project_id = os.getenv('DIALOG_PROJECT_ID')


def detect_intent_texts(session_id, text, language_code):
    """Отправялем текст сообщения в Dialog Flow и получаем ответ"""

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(dialog_project_id, session_id)

    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)

    return response.query_result.fulfillment_text
