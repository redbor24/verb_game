import logging
import random

import vk_api
from environs import Env
from vk_api.longpoll import VkEventType, VkLongPoll

import config
from gflow import detect_intent_texts

logger = logging.getLogger('vkbot')


def answer(event, api):
    logger.info(f'Вопрос: {event.text}')
    is_query_responsed, answer_text = detect_intent_texts(google_project_id, google_project_id, event.text, 'ru-RU')
    if is_query_responsed:
        api.messages.send(user_id=event.user_id, message=answer_text, random_id=random.randint(1, 1000))
        logger.info(f'Ответ: {answer_text}')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    log_formatter = logging.Formatter(fmt=config.log_format, datefmt=config.log_date_format)

    fh = logging.FileHandler(filename='verbgame_vk.log', encoding='utf-8')
    fh.setLevel(logging.INFO)
    fh.setFormatter(log_formatter)
    logger.addHandler(fh)

    env = Env()
    env.read_env()
    google_project_id = env('GOOGLE_PROJECT_ID')

    vk_token = env('VK_TOKEN')
    vk_session = vk_api.VkApi(token=vk_token)
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)
    for vk_event in longpoll.listen():
        if vk_event.type == VkEventType.MESSAGE_NEW and vk_event.to_me:
            answer(vk_event, vk_api)
