import logging
import random

import vk_api
from environs import Env
from vk_api.longpoll import VkEventType, VkLongPoll

from gflow import detect_intent_texts

logging.basicConfig(
    filename='verbgame_vk.log',
    encoding='utf-8',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger('vkbot')


def answer(event, api):
    message = detect_intent_texts(google_project_id, google_project_id, event.text, 'ru-RU')
    if message:
        api.messages.send(user_id=event.user_id, message=message, random_id=random.randint(1, 1000))


if __name__ == "__main__":
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
