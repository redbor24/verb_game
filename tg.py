import logging

from environs import Env
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, MessageHandler,
                          Updater)
from telegram.ext.filters import Filters

import config
from gflow import detect_intent_texts

logger = logging.getLogger('tgbot')


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(f'Здравствуйте, {user.username}!')


def answer(update: Update, context: CallbackContext) -> None:
    if update.message:
        message = detect_intent_texts(google_project_id, google_project_id, update.message.text, 'ru-RU')
        if message:
            update.message.reply_text(message)
        else:
            update.message.reply_text(update.message.text)
        logger.info(update.message.text)


def main() -> None:
    logger.info('Начало работы')
    updater = Updater(tg_token)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, answer))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    log_formatter = logging.Formatter(fmt=config.log_format, datefmt=config.log_date_format)

    fh = logging.FileHandler(filename='verbgame_tg.log', encoding='utf-8')
    fh.setLevel(logging.INFO)
    fh.setFormatter(log_formatter)
    logger.addHandler(fh)

    env = Env()
    env.read_env()
    tg_token = env('TG_TOKEN')
    google_project_id = env('GOOGLE_PROJECT_ID')

    main()
