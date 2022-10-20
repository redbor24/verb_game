import json

from environs import Env

import google.cloud.dialogflow as dialogflow
import argparse


class QuestionNotFound(Exception):
    pass


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print(f'Интент "{response.display_name}" создан')


if __name__ == '__main__':
    env = Env()
    env.read_env()
    google_project_id = env('GOOGLE_PROJECT_ID')

    parser = argparse.ArgumentParser(description='New intent')
    parser.add_argument('file', type=str, help='Файл с данными для интента')
    parser.add_argument('intent', type=str, help='Название интента')
    args = parser.parse_args()

    intent_name = args.intent
    with open(args.file, "r", encoding='utf-8') as my_file:
        questions = json.load(my_file)

    if not any(True for question in questions if question == intent_name):
        raise QuestionNotFound(f'Вопрос "{intent_name}" не найден в файле')
    # exit()

    for question in questions:
        if question == intent_name:
            create_intent(google_project_id, question,
                          questions[question]['questions'],
                          [questions[question]['answer']])
            break
