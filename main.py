# import os

import telebot
from telebot.types import Message

bot = telebot.TeleBot('886072920:AAGP_OzHa8bv_s90OSk6mF-HJonxlfEfnbw')


# TODO: сделать регу
@bot.message_handler(commands=['start'])
def welcome(message: Message):
    bot.send_message(
        text="Привет, я помогу тебе отслеживать скидки на книги!\n"
             "Чтобы добавить книгу, напиши:\n`добавить [ссылка на книгу]`",

        chat_id=message.from_user.id, parse_mode='Markdown')


@bot.message_handler(func=lambda message: True)
def upper(message: Message):
    bot.send_message(message.chat.id, "Бот временно не работает. Приносим извинения за доставленные неудобства.")


bot.polling()
