import logging

from environs import Env
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Updater
from telegram.ext.filters import Filters

from gflow import detect_intent_texts

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
env = Env()
env.read_env()
tg_token = env('TG_TOKEN')
google_project_id = env('GOOGLE_PROJECT_ID')


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_text(f'Здравствуйте, {user.username}!')


def echo(update: Update, context: CallbackContext) -> None:
    message = detect_intent_texts(google_project_id, google_project_id, update.message.text, 'ru-RU')
    if message:
        update.message.reply_text(message)
    else:
        logger.info(f'Не понимай: "{update.message.text}"')


def main() -> None:
    updater = Updater(tg_token)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
