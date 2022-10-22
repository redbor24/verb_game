import random

import vk_api
from environs import Env
from vk_api.longpoll import VkEventType, VkLongPoll

from gflow import detect_intent_texts

env = Env()
env.read_env()
google_project_id = env('GOOGLE_PROJECT_ID')


def echo(event, vk_api):
    message = detect_intent_texts(google_project_id, google_project_id, [event.text], 'ru-RU')
    vk_api.messages.send(
        user_id=event.user_id,
        message=message,
        random_id=random.randint(1, 1000)
    )
    print(f'echo: {message}')


if __name__ == "__main__":
    vk_token = env('VK_TOKEN')
    vk_session = vk_api.VkApi(token=vk_token)
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)
