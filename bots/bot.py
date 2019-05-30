import json
import os
import time

import apiai
import telebot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

import detail
import logger
from databases.database import Database
from parsers.parser_manager import ParserManager


class Bot:
    def __init__(self):
        self.bot = telebot.TeleBot(os.environ.get("token"))

        self.book_to_delete = {}
        self.book_to_add = {}

    def typing(self, secs, message: Message):
        self.bot.send_chat_action(message.chat.id, "typing")
        time.sleep(secs)

    def uploading_photo(self, secs, message: Message):
        self.bot.send_chat_action(message.chat.id, "upload_photo")
        time.sleep(secs)

    def start_user(self, message: Message):
        """Send a welcome message to the user and makes his status active."""

        logger.show_msg(message)
        database = Database()
        database.start_following(message.chat.id)
        self.typing(1, message)
        self.bot.send_message(chat_id=message.from_user.id, parse_mode='Markdown',
                              text="Привет, я помогу тебе отслеживать скидки на книги!\n"
                                   "Чтобы добавить книгу, напиши:\n`добавить [ссылка на книгу]`")

    def show_list(self, message: Message):
        """
        Show a list of subscriptions from the database, attaching a delete button.

        If the user does not exist or the list is empty,
         then the message that the list is empty is displayed.
        """

        logger.show_msg(message)
        database = Database()
        parser = ParserManager()
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Удалить", callback_data="delete_book"))

        subscriptions = database.get_subscriptions(message.chat.id)

        if subscriptions == [None] or not subscriptions:
            self.typing(0.3, message)
            self.bot.send_message(message.chat.id, "Кажется, ничего нет 🤕")

        else:
            for subscription in database.get_subscriptions(message.chat.id):
                detail_book = parser.parsing_book(subscription)
                self.uploading_photo(0.2, message)
                reply_msg = self.bot.send_photo(chat_id=message.chat.id,
                                                photo=open(f"images/{detail_book['image_name']}", 'rb'),
                                                caption=f"{detail_book['title']} ({detail_book['price']}р.)",
                                                reply_markup=markup)

                self.book_to_delete[reply_msg.message_id] = detail_book

    def show_help(self, message: Message):
        """Send a message to the user with prompts."""

        logger.show_msg(message)
        self.typing(2, message)
        self.bot.send_message(chat_id=message.chat.id,
                              text="Я, как чистокровный робот, помогу тебе не сойти с ума в мире книжных скидок 🤖\n"
                                   "*нет, я не уничтожу мир 🙄*\n\n"
                                   "Если ты хочешь включить активный режим, то добавь новую книгу или отправь /start\n"
                                   "Если же ты хочешь выключить активный режим и впредь не получать сообщений, "
                                   "отправь /stop\n"
                                   "Хочешь посмотреть свои подписки или удалить книгу? Нажимай /list\n"
                                   "Хочешь посмотреть на код или кинуть донат? Тебе сюда /about")

    def show_about(self, message: Message):
        """Send a message to the user with information about the author."""

        logger.show_msg(message)
        self.typing(1, message)
        self.bot.send_message(chat_id=message.chat.id, parse_mode='Markdown',
                              text="`Я являюсь небольшим пет-проектом для трекинга скидок 🤖\n"
                                   "Хотите увидеть внутренности?\nВаша воля, господин!`\n"
                                   "https://github.com/ars-kalinichenko/BookSalesBot")

    def stop_user(self, message: Message):
        """Make the subscriber inactive."""

        logger.show_msg(message)
        database = Database()
        database.stop_following(message.chat.id)
        self.typing(1, message)
        self.bot.send_message(chat_id=message.chat.id, text="Прощайте.\n"
                                                            "Надеемся, вы вернётесь 😌")

    def small_talk(self, message: Message):
        """Allow you to communicate with the bot using DialogFlow."""

        logger.show_msg(message)
        request = apiai.ApiAI(os.environ.get("smalltalk")).text_request()
        request.lang = 'ru'
        request.query = message.text
        response_json = json.loads(request.getresponse().read().decode('utf-8'))
        response = response_json['result']['fulfillment']['speech']
        self.typing(1, message)

        logger.show_msg(self.bot.send_message(chat_id=message.from_user.id, text=response))

    def adding_book(self, message: Message):
        """
        Respond to a message asking to add, and then
         asks the user to add a book to the subscription using the buttons.

        If the link is not valid, then a message is sent asking
         to enter the correct link and the error is logged
        If the image does not exist, only text is sent.
        """

        logger.show_msg(message)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Да", callback_data="add_link"))
        markup.add(InlineKeyboardButton(text="Нет", callback_data="no_add_link"))
        parser = ParserManager()

        try:
            link = message.text.lower().split('добавить')[-1].strip()
            book = parser.parsing_book(link)
            image_path = f"images/{book['image_name']}"
            case_rub = f'рубл{detail.ruble_cases[book["price"] % 100]}'

            if os.path.exists(image_path):
                self.uploading_photo(0.5, message)
                reply_msg = self.bot.send_photo(message.chat.id,
                                                photo=open(image_path, 'rb'),
                                                caption='Вы уверены, что хотите добавить:\n'
                                                f'"{book["title"]}" за {book["price"]} {case_rub}?',
                                                reply_markup=markup)

                logger.show_caption_photo(reply_msg)
            else:
                reply_msg = self.bot.send_message(message.chat.id,
                                                  text='Вы уверены, что хотите добавить:\n'
                                                  f'"{book["title"]}" за {book["price"]} {case_rub}?',
                                                  reply_markup=markup)
            self.book_to_add[reply_msg.message_id] = book
            logger.show_msg(reply_msg)

        except (TypeError, AttributeError) as error:
            logger.show_error(system="Bot.adding_book()", error=repr(error))
            self.bot.send_message(message.chat.id, "Введите правильную ссылку!")

    def send_notification(self, chat_id: int, book_detail: dict, sale: int):
        """Notify the follower of a book discount."""

        notification = self.bot.send_photo(chat_id, photo=open(f"images/{book_detail['image_name']}", 'rb'),
                                           caption=f'Книга "{book_detail["title"]}"\n'
                                           f'подешевела на {sale}% ({book_detail["price"]}р.)')
        logger.show_caption_photo(notification)

    def callback_handler(self, call):
        """Button Handling Method."""

        if call.data == 'add_link':
            try:
                self.___add_book(call)
            except KeyError as er:
                self.bot.answer_callback_query(callback_query_id=call.id,
                                               text='Попробуйте отправить ссылку ещё раз ❌')
                logger.show_error(system="Bot.book_to_db()", error=repr(er))
            else:
                self.bot.answer_callback_query(callback_query_id=call.id, text='Книга добавлена в список ✅')

        elif call.data == 'no_add_link':
            self.bot.answer_callback_query(callback_query_id=call.id, text='Отменяем запуск боеголовок, сэр 👨🏼‍✈️')

        elif call.data == "delete_book":
            self.__delete_book(call)

        try:
            self.bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                               message_id=call.message.message_id)
            self.book_to_add.pop(call.message.message_id)
        except:
            pass

    def __delete_book(self, call):
        """Remove a book from subscriptions."""

        database = Database()
        try:
            link = self.book_to_delete[call.message.message_id]['link']
            database.delete_subscription(call.message.chat.id, link)
        except KeyError:
            self.bot.answer_callback_query(callback_query_id=call.id, text='Попробуйте ещё раз 🐙')
        else:
            self.bot.answer_callback_query(callback_query_id=call.id, text='Книга удалена 🦄')

    def ___add_book(self, call):
        """Add a book from subscriptions."""

        database = Database()
        book_ = self.book_to_add[call.message.message_id]
        database.insert_book(book_, [call.message.chat.id])
        database.insert_follower([book_['link']], call)
        database.start_following(call.message.chat.id)
