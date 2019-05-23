import json
import os
import time

import apiai
import telebot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

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

        if self.book is not None:
            self.book['follower'] = [message.chat.id]

        try:
            case_rub = f'рубл{detail.ruble_cases[self.book["price"] % 10]}'
            self.typing(1, message)
            self.bot.send_photo(message.chat.id, photo=open(f"images/{self.book['image_name']}", 'rb'),
                                caption='Вы уверены, что хотите добавить:\n'
                                f'"{self.book["title"]}" за {self.book["price"]} {case_rub}?',
                                reply_markup=markup)
        except TypeError:
            self.bot.send_message(message.chat.id, "Введите правильную ссылку!")

        logger.show_msg(message)

    def welcome(self, message: Message):
        self.typing(1, message)
        self.bot.send_message(
            text="Привет, я помогу тебе отслеживать скидки на книги!\n"
                 "Чтобы добавить книгу, напиши:\n`добавить [ссылка на книгу]`",

            chat_id=message.from_user.id, parse_mode='Markdown')
        logger.show_msg(message)

    def small_talk(self, message: Message):
        request = apiai.ApiAI(os.environ.get("smalltalk")).text_request()
        request.lang = 'ru'
        request.query = message.text
        response_json = json.loads(request.getresponse().read().decode('utf-8'))
        response = response_json['result']['fulfillment']['speech']
        self.typing(1, message)
        logger.show_msg(message)
        logger.show_msg(self.bot.send_message(chat_id=message.from_user.id, text=response))

    def book_to_db(self, call):
        if call.data == 'add_url':
            database = Database()
            insert_result = database.insert_book(self.book)

            if insert_result is False:
                self.bot.answer_callback_query(callback_query_id=call.id,
                                               text='Попробуйте отправить ссылку ещё раз ❌')

            else:
                self.bot.answer_callback_query(callback_query_id=call.id, text='Книга добавлена в список ✅')

        elif call.data == 'no_add_url':
            self.bot.answer_callback_query(callback_query_id=call.id, text='Отменяем запуск боеголовок, сэр!')

        self.bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                           message_id=call.message.message_id)
