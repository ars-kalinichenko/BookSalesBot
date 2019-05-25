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
        self.queue_book = {}
        self.bot = telebot.TeleBot(os.environ.get("token"))
        self.book = {}

    def typing(self, secs, message: Message):
        self.bot.send_chat_action(message.chat.id, "typing")
        time.sleep(secs)

    # TODO: sending photo

    def welcome(self, message: Message):
        database = Database()
        database.start_following(message.chat.id)
        self.typing(1, message)
        self.bot.send_message(chat_id=message.from_user.id, parse_mode='Markdown',
                              text="Привет, я помогу тебе отслеживать скидки на книги!\n"
                                   "Чтобы добавить книгу, напиши:\n`добавить [ссылка на книгу]`")
        logger.show_msg(message)

    def show_list(self, message: Message):
        self.typing(3, message)

    def show_help(self, message: Message):
        self.typing(1, message)
        self.bot.send_message(chat_id=message.chat.id,
                              text="Я, как чистокровный робот, помогу тебе не сойти с ума в мире книжных скидок 🤖\n"
                                   "*нет, я не уничтожу мир 🙄*\n\n"
                                   "Если ты хочешь включить активный режим, то добавь новую книгу или отправь /start\n"
                                   "Если же ты хочешь выключить активный режим и впредь не получать сообщений, "
                                   "отправь /stop\n"
                                   "Хочешь посмотреть свои подписки или удалить книгу? Нажимай /list\n"
                                   "Хочешь посмотреть на код или кинуть донат? Тебе сюда /about")

    def show_about(self, message: Message):
        self.typing(1, message)
        self.bot.send_message(chat_id=message.chat.id, parse_mode='Markdown',
                              text="`Я являюсь небольшим пет-проектом для трекинга скидок 🤖\n"
                                   "Хотите увидеть внутренности?\nВаша воля, господин!`\n"
                                   "https://github.com/ars-kalinichenko/BookSalesBot")

    def stop_user(self, message: Message):
        database = Database()
        database.stop_following(message.chat.id)
        self.typing(1, message)
        self.bot.send_message(chat_id=message.chat.id, text="Прощайте. Надеемся, вы вернётесь 😌")

    def small_talk(self, message: Message):
        request = apiai.ApiAI(os.environ.get("smalltalk")).text_request()
        request.lang = 'ru'
        request.query = message.text
        response_json = json.loads(request.getresponse().read().decode('utf-8'))
        response = response_json['result']['fulfillment']['speech']
        self.typing(1, message)
        logger.show_msg(message)
        logger.show_msg(self.bot.send_message(chat_id=message.from_user.id, text=response))

    def adding_book(self, message: Message):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Да", callback_data="add_url"))
        markup.add(InlineKeyboardButton(text="Нет", callback_data="no_add_url"))

        try:
            url = message.text.split(' ')[-1]
            self.book = parser_manager.add_book(url)

            self.queue_book[message.chat.id] = self.book.copy()

            case_rub = f'рубл{detail.ruble_cases[self.book["price"] % 100]}'
            self.typing(1, message)

            self.bot.send_photo(message.chat.id,
                                photo=open(f"images/{self.book['image_name']}", 'rb'),
                                caption='Вы уверены, что хотите добавить:\n'
                                f'"{self.book["title"]}" за {self.book["price"]} {case_rub}?',
                                reply_markup=markup)
        except TypeError:
            self.bot.send_message(message.chat.id, "Введите правильную ссылку!")

        logger.show_msg(message)

    def book_to_db(self, call):
        if call.data == 'add_url':
            database = Database()

            book_ = self.queue_book[call.message.chat.id]

            try:
                database.insert_book(book_, [call.message.chat.id])
                database.insert_follower([book_['link']], call)
            except KeyError as er:
                self.bot.answer_callback_query(callback_query_id=call.id,
                                               text='Попробуйте отправить ссылку ещё раз ❌')
                logger.show_error(system="Bot.book_to_db()", error=repr(er))
            else:
                self.bot.answer_callback_query(callback_query_id=call.id, text='Книга добавлена в список ✅')
                database.start_following(call.message.chat.id)

        elif call.data == 'no_add_url':
            self.bot.answer_callback_query(callback_query_id=call.id, text='Отменяем запуск боеголовок, сэр!')

        self.bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                           message_id=call.message.message_id)

        self.queue_book.pop(call.message.chat.id)
