import os

import telebot
from telebot.types import Message

import logger

bot = telebot.TeleBot(os.environ.get("token"))


@bot.message_handler(commands=['start'])
def welcome(message: Message):
    bot.send_message(
        text="Привет, я помогу тебе отслеживать скидки на книги!\n"
             "Чтобы добавить книгу, напиши:\n`добавить [ссылка на книгу]`",

        chat_id=message.from_user.id, parse_mode='Markdown')
    logger.push_msg_to_log(message)


@bot.message_handler(func=lambda message: True)
def upper(message: Message):
    bot.send_message(message.chat.id, "Бот временно не работает. Приносим извинения за доставленные неудобства.")
    logger.push_msg_to_log(message)
    with open('message.log', 'w') as file:
        file.write(message.text)


bot.polling()
