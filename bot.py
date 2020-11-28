import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
import requests
import json
import random as rd
TOKEN = 'Telegram Token Here'
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def access_key():
    key = '{Client_id Here}'
    return key


Welcome_Msg = '''<b> Hey there </b>
<b> I am The Wallpaper bot</b>🤖🤖🤖🤖
<b> I Can Provide U with Some Cool Pics from unsplash.com</b>
<b>Hit /help to get Started</b> 🦾🦾🦾'''

Help_Msg = '''Hit /random to get a random Image
Or just send me a Key word to get an image related to it😉😉'''

unsplash_url = "https://unsplash.com/"


def start(update, context):
    update.message.reply_html(Welcome_Msg)


def help_cmd(update, context):
    update.message.reply_text(Help_Msg)


def random(update, context):
    url = "https://api.unsplash.com/photos/random/?client_id=" + access_key()
    chat_id = update.message.chat_id
    data = requests.get(url).json()
    try:
        photo_url = data['urls']['regular']
        download_url_data = data['links']['download_location'] + \
            '/?client_id='+access_key()
        download_url = requests.get(download_url_data).json()['url']
        photo_html = data['links']['html']
        photographer_name = data['user']['name']
        photographer_page = data['user']['links']['html']
        context.bot.send_photo(chat_id=chat_id, photo=photo_url,
                               caption=f'[Photo]({photo_url}) '
                               f'by [{photographer_name}]({photographer_page}) '
                               f'on [Unsplash]({unsplash_url})',
                               parse_mode='MARKDOWN')
        context.bot.send_document(
            chat_id=chat_id, document=download_url, caption="Uncompressed Image! Enjoy 😊😊")
    except Exception:
        update.message.reply_text('Oh Something is wrong 😯😯 ! try later')


def custom_search(update, context):
    query = update.message.text
    chat_id = update.message.chat_id
    url = f"https://api.unsplash.com/search/?client_id={access_key()}&query={query}"
    fullData = requests.get(url).json()
    try:
        data = rd.choice(fullData["photos"]["results"])
        photo_url = data['urls']['regular']
        download_url_data = data['links']['download_location'] + \
            '/?client_id='+access_key()
        download_url = requests.get(download_url_data).json()['url']
        photo_html = data['links']['html']
        photographer_name = data['user']['name']
        photographer_page = data['user']['links']['html']
        context.bot.send_photo(chat_id=chat_id, photo=photo_url,
                               caption=f'[Photo]({photo_url}) '
                               f'by [{photographer_name}]({photographer_page}) '
                               f'on [Unsplash]({unsplash_url})',
                               parse_mode='MARKDOWN')
        context.bot.send_document(
            chat_id=chat_id, document=download_url, caption="Uncompressed Image! Enjoy 😊😊")
    except Exception:
        update.message.reply_text('Oh Something is wrong 😯😯 ! try later')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)
    PORT = int(os.environ.get('PORT', '8443'))
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_cmd))
    dp.add_handler(CommandHandler("random", random))
    dp.add_handler(MessageHandler(Filters.text, custom_search))
    # log all errors
    dp.add_error_handler(error)
    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.set_webhook(
        "https://awesomewallbot.herokuapp.com/" + TOKEN)
    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
