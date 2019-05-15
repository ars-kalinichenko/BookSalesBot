import os

import telebot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

import ioc
import detail
import logger
from bot import action
from parsers import parser_manager

bot = telebot.TeleBot(os.environ.get("token"))
action = action.BotAction()

markup = InlineKeyboardMarkup()
markup.add(InlineKeyboardButton(text="Да", callback_data="add_url"))
markup.add(InlineKeyboardButton(text="Нет", callback_data="no_add_url"))


@bot.message_handler(commands=['start'])
def welcome(message: Message):
    action.typing(1, message)
    bot.send_message(
        text="Привет, я помогу тебе отслеживать скидки на книги!\n"
             "Чтобы добавить книгу, напиши:\n`добавить [ссылка на книгу]`",

        chat_id=message.from_user.id, parse_mode='Markdown')
    logger.show_msg(message)


@bot.message_handler(content_types=['text'])
def reply(message: Message):
    if "добавить" in message.text.lower():
        url = message.text.split(' ')[-1]
        ioc.queue_url.put(url)

        action.typing(1, message)
        bot.send_message(message.chat.id, "Хмм")
        book = parser_manager.add_book(url)
        try:
            case_rub = f'рубл{detail.ruble_cases[book["price"] % 10]}'
            action.typing(2, message)
            bot.send_message(message.chat.id,
                             f'Вы уверены,что хотите добавить "{book["title"]}" за {book["price"]} {case_rub}?',
                             reply_markup=markup)
        except TypeError:
            bot.send_message(message.chat.id, "Введите правильную ссылку!")

    else:
        action.typing(2, message)
        bot.send_message(message.chat.id, "Бот временно не работает. Приносим извинения за доставленные неудобства.")
    logger.show_msg(message)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'add_url':
        bot.answer_callback_query(callback_query_id=call.id, text='Книга добавлена в список.')

    bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)


bot.polling()
