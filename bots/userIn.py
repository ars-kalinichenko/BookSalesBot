from telebot.types import Message

from bots import bot

bot_action = bot.Bot()
bot = bot_action.bot


@bot.message_handler(commands=['start'])
def start(message: Message):
    bot_action.start_user(message)


@bot.message_handler(commands=['list'])
def listing(message: Message):
    bot_action.show_list(message)


@bot.message_handler(commands=['help'])
def support(message: Message):
    bot_action.show_help(message)


@bot.message_handler(commands=['about'])
def about(message: Message):
    bot_action.show_about(message)


@bot.message_handler(commands=['stop'])
def stop(message: Message):
    bot_action.stop_user(message)


@bot.message_handler(content_types=['text'])
def small_talk(message: Message):
    if "добавить" in message.text.lower():
        bot_action.adding_book(message)
    else:
        bot_action.small_talk(message)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot_action.book_to_db(call)


def main():
    bot.polling()
