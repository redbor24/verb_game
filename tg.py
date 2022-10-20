import logging
import google.cloud.dialogflow as dialogflow

from environs import Env
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, MessageHandler,
                          Updater)
from telegram.ext.filters import Filters

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
    update.message.reply_text('Здравствуйте!')


def echo(update: Update, context: CallbackContext) -> None:
    message = detect_intent_texts(google_project_id, google_project_id, [update.message.text], 'ru-RU')
    update.message.reply_text(message)


def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        # print("=" * 20)
        # print("Query text: {}".format(response.query_result.query_text))
        # print(
        #     "Detected intent: {} (action {}, confidence: {})\n".format(
        #         response.query_result.intent.display_name,
        #         response.query_result.action,
        #         response.query_result.intent_detection_confidence
        #     )
        # )
        # print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))
    return response.query_result.fulfillment_text



def main() -> None:
    # env = Env()
    # env.read_env()
    # tg_token = env('TG_TOKEN')
    # google_project_id = env('GOOGLE_PROJECT_ID')
    #
    # texts = [
    #     'Здравствуй, железяка',
    #     'и прощай...'
    # ]
    # detect_intent_texts(google_project_id, 'google_project_id', texts, 'ru-RU')
    # exit()

    updater = Updater(tg_token)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
