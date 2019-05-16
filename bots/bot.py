import time

import telebot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import os
import detail
import logger
from databases.database import Database
from parsers import parser_manager


class Bot:
    def __init__(self):
        self.bot = telebot.TeleBot(os.environ.get("token"))
        self.book = {}

    def typing(self, secs, message: Message):
        self.bot.send_chat_action(message.chat.id, "typing")
        time.sleep(secs)

    def adding_book(self, message: Message):

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Да", callback_data="add_url"))
        markup.add(InlineKeyboardButton(text="Нет", callback_data="no_add_url"))

        url = message.text.split(' ')[-1]

        self.book = parser_manager.add_book(url)

        self.typing(2, message)
        self.bot.send_message(message.chat.id, "Хмм")

        self.book['follower'] = [message.from_user.id]

        try:
            case_rub = f'рубл{detail.ruble_cases[self.book["price"] % 10]}'
            self.typing(2, message)
            self.bot.send_message(message.chat.id,
                                  (f'Вы уверены, что хотите добавить: \n'
                                   f'"{self.book["title"]}" за {self.book["price"]} {case_rub}?'),
                                  reply_markup=markup)
        except TypeError:
            self.bot.send_message(message.chat.id, "Введите правильную ссылку!")

    def welcome(self, message: Message):
        self.typing(1, message)
        self.bot.send_message(
            text="Привет, я помогу тебе отслеживать скидки на книги!\n"
                 "Чтобы добавить книгу, напиши:\n`добавить [ссылка на книгу]`",

            chat_id=message.from_user.id, parse_mode='Markdown')
        logger.show_msg(message)

    def small_talk(self, message: Message):
        self.typing(2, message)
        self.bot.send_message(message.chat.id,
                              "Бот временно не работает. Приносим извинения за доставленные неудобства.")

    def book_to_db(self, call):
        if call.data == 'add_url':
            database = Database()
            database.insert_book(self.book)
            self.bot.answer_callback_query(callback_query_id=call.id, text='Книга добавлена в список.')

        self.bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                           message_id=call.message.message_id)