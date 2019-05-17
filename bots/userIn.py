from telebot.types import Message

import logger
from bots import bot

bot_action = bot.Bot()
bot = bot_action.bot


@bot.message_handler(commands=['start'])
def welcome(message: Message):
    bot_action.welcome(message)


@bot.message_handler(content_types=['text'])
def reply(message: Message):
    if "добавить" in message.text.lower():
        bot_action.adding_book(message)
    else:
        bot_action.small_talk(message)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot_action.book_to_db(call)


bot.polling()
