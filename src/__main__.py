from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from src.auth import authenticate
from src.imgur_upload import imgur_upload
from src.IArequest import request_respbai
import configparser

config = configparser.ConfigParser()
config.read('auth.ini')
TOKEN = config.get('credentials', 'BOT_TOKEN')


# Handles the image, download it and upload to imgur
def hand_actions(bot, update):
    file = bot.getFile(update.message.photo[-1].file_id)
    file.download('image.jpg')
    # Upload the image to imgur
    image = imgur_upload(client)
    bot.sendMessage(chat_id=update.message.chat_id, text="Upload successful")
    url = image['link']

    response_jsons = request_respbai(url)
    text = "\n".join(response_jsons)
    bot.sendMessage(chat_id=update.message.chat_id, text=text)


# Displays the start message when '/start' is handled
def help(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Send an image file to get te IA response")


if __name__ == '__main__':
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('help', help))

    client = authenticate()

    image_handler = MessageHandler(Filters.photo, hand_actions)
    dp.add_handler(image_handler)
    updater.start_polling()
    updater.idle()
