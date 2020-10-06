import os
import json

import dialogflow_v2

dialog_project_id = os.getenv('DIALOG_PROJECT_ID')


def create_intents():
    """Создаем интенты с вопросами и ответами из файла questions.json"""
    with open('questions.json', 'r') as qf:
        questions = json.load(qf)
        client = dialogflow_v2.IntentsClient()
        parent = client.project_agent_path(dialog_project_id)

        for title, question in questions.items():
            intent = {
                "display_name": title,
                "messages": [{"text": {"text": [question['answer']]}}],
                "training_phrases": [{"parts": [{"text": q_text}]} for q_text in question.get('questions')]
            }
            try:
                client.create_intent(parent, intent)
            except Exception as e:
                if 'already exists' in str(e):
                    print('Интент уже существует')
                else:
                    raise e


def train_agent():
    """Запускаем обучение по созданым интентам"""

    client = dialogflow_v2.AgentsClient()
    parent = client.project_path(dialog_project_id)
    client.train_agent(parent)


if __name__ == '__main__':
    create_intents()
    train_agent()
