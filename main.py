import telebot
from telebot.types import Message
import os
import logger

bot = telebot.TeleBot(os.environ.get("token"))


@bot.message_handler(commands=['start'])
def welcome(message: Message):
    bot.send_message(
        text="Привет, я помогу тебе отслеживать скидки на книги!\n"
             "Чтобы добавить книгу, напиши:\n`добавить [ссылка на книгу]`",

        chat_id=message.from_user.id, parse_mode='Markdown')
    logger.show_msg(message)


@bot.message_handler(func=lambda message: True)
def upper(message: Message):
    bot.send_message(message.chat.id, "Бот временно не работает. Приносим извинения за доставленные неудобства.")
    logger.show_msg(message)


bot.polling()
