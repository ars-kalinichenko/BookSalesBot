import os

import telebot
from telebot.types import Message

import IOC
import logger
from parsers import parser_manager

bot = telebot.TeleBot(os.environ.get("token"))


@bot.message_handler(commands=['start'])
def welcome(message: Message):
    bot.send_message(
        text="Привет, я помогу тебе отслеживать скидки на книги!\n"
             "Чтобы добавить книгу, напиши:\n`добавить [ссылка на книгу]`",

        chat_id=message.from_user.id, parse_mode='Markdown')
    logger.show_msg(message)


@bot.message_handler(content_types=['text'])
def reply(message: Message):
    if "добавить" in message.text.lower():
        IOC.queue_url.put(message.text.split(' ')[-1])
        bot.send_message(message.chat.id, "Хмм")
        book = parser_manager.add_book(IOC.queue_url[0])
        bot.send_message(message.chat.id,
                         f"Вы уверены,что хотите добавить книгу {book['title']} за {book['price']} рублей?")
    else:
        bot.send_message(message.chat.id, "Бот временно не работает. Приносим извинения за доставленные неудобства.")
    logger.show_msg(message)


bot.polling()
