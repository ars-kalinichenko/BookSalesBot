import logging

from telebot.types import Message


def show_msg(message: Message):
    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)
    if message.from_user.username is None:
        logging.info('{} sent "{}"'.format("Anonymous", message.text))
    else:
        logging.info('{} sent "{}"'.format(message.from_user.username, message.text))


def show_error(**kwargs):
    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)

    logging.debug('{} sent "{}"'.format(kwargs['system'], kwargs['error']))
