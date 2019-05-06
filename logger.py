import logging

from telebot.types import Message


def push_msg_to_cout(message: Message):
    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)

    logging.info('{} sent "{}"'.format(message.from_user.username, message.text))


def push_error_cout(**kwargs):
    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)

    logging.debug('{} sent "{}"'.format(kwargs['system'], kwargs['error']))
