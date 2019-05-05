import logging

from telebot.types import Message


def push_msg_to_log(message: Message):
    logging.basicConfig(filename='message.log',
                        filemode='w',
                        format='%(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)

    logging.info('{} sent "{}"'.format(message.from_user.username, message.text))
