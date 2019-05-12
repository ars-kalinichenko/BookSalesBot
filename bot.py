import time
import os
import telebot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

import IOC
import detail
import logger
from parsers import parser_manager

bot = telebot.TeleBot(os.environ.get("token"))


def bot_typing(message: Message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1)


@bot.message_handler(commands=['start'])
def welcome(message: Message):
    bot_typing(message)
    bot.send_message(
        text="Привет, я помогу тебе отслеживать скидки на книги!\n"
             "Чтобы добавить книгу, напиши:\n`добавить [ссылка на книгу]`",

        chat_id=message.from_user.id, parse_mode='Markdown')
    logger.show_msg(message)


@bot.message_handler(content_types=['text'])
def reply(message: Message):
    if "добавить" in message.text.lower():
        url = message.text.split(' ')[-1]
        IOC.queue_url.put(url)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Да", callback_data="add_url"))
        markup.add(InlineKeyboardButton(text="Нет", callback_data="no_add_url"))
        bot.send_message(message.chat.id, "Хмм")
        book = parser_manager.add_book(url)
        case_rub = f'рубл{detail.ruble_cases[book["price"] % 10]}'
        bot.send_message(message.chat.id,
                         f'Вы уверены,что хотите добавить "{book["title"]}" за {book["price"]} {case_rub}?',
                         reply_markup=markup)
    else:
        bot_typing(message)
        bot.send_message(message.chat.id, "Бот временно не работает. Приносим извинения за доставленные неудобства.")
    logger.show_msg(message)


bot.polling()
