import os
import time

import telebot
from telebot.types import Message


class BotAction:
    def __init__(self):
        self.bot = telebot.TeleBot(os.environ.get("token"))

    def typing(self, secs: int, msg: Message):
        self.bot.send_chat_action(msg.chat.id, "typing")
        time.sleep(secs)
