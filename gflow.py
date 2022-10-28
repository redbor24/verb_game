import argparse
import json
import logging

import google.cloud.dialogflow as dialogflow
from environs import Env

import config

logger = logging.getLogger('google')


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
        request={'parent': parent, 'intent': intent}
    )

    logger.info(f'Интент создан: "{response.display_name}"')


def detect_intent_texts(project_id, session_id, query, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=query, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(request={'session': session, 'query_input': query_input})
    if not response.query_result.intent.is_fallback:
        return response.query_result.fulfillment_text


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    log_formatter = logging.Formatter(fmt=config.log_format, datefmt=config.log_date_format)

    fh = logging.FileHandler(filename='verbgame_gflow.log', encoding='utf-8')
    fh.setLevel(logging.INFO)
    fh.setFormatter(log_formatter)
    logger.addHandler(fh)

    env = Env()
    env.read_env()
    google_project_id = env('GOOGLE_PROJECT_ID')

    parser = argparse.ArgumentParser(description='New intent')
    parser.add_argument('file', type=str, help='Файл с данными для интента')
    parser.add_argument('-in', '--intent_name', type=str, help='Название интента')
    args = parser.parse_args()
    args_intent_name = args.intent_name

    with open(args.file, 'r', encoding='utf-8') as my_file:
        intents = json.load(my_file)

    if args_intent_name:
        try:
            intent = intents[args_intent_name]
            create_intent(google_project_id, args_intent_name, intent['questions'], intent['answer'])
        except KeyError as name_not_found_exc:
            logger.error(f'Вопрос не найден: {args_intent_name}')
        except Exception as create_intent_exc:
            logger.error(f'Ошибка создания интента "{args_intent_name}": {create_intent_exc}')
    else:
        for intent_name in intents:
            intent = intents[intent_name]
            try:
                create_intent(google_project_id, intent_name, intent['questions'], intent['answer'])
            except Exception as create_intent_exc:
                logger.error(f'Ошибка создания интента "{intent_name}": {create_intent_exc}')
