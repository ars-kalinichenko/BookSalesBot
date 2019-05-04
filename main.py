import os

import telebot
from telebot.types import Message

bot = telebot.TeleBot(os.environ.get("token"))


# TODO: сделать регу
@bot.message_handler(commands=['start'])
def welcome(message: Message):
    bot.send_message(
        text="Привет, я помогу тебе отслеживать скидки на книги!\n"
             "Чтобы добавить книгу, напиши:\n`добавить [ссылка на книгу]`",

        chat_id=message.from_user.id, parse_mode='Markdown')


@bot.message_handler(func=lambda message: True)
def upper(message: Message):
    bot.reply_to(message, "Посмотри аниме, а не трать время впустую!".upper())


bot.polling()
