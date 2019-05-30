import logging

from telebot.types import Message


def show_msg(message: Message):
    """
    Logs the text of the message and its author.
    If the user does not have a nickname, then author = anonymous.
    """
    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)
    if message.from_user.username is None:
        logging.info('{} sent "{}"'.format("Anonymous", message.text))
    else:
        logging.info('{} sent "{}"'.format(message.from_user.username, message.text))


def show_caption_photo(message: Message):
    """
    Logs the caption of the photo and the author.
    If the user does not have a nickname, then author = anonymous.
    """

    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)
    if message.from_user.username is None:
        logging.info('{} sent "{}"'.format("Anonymous", message.caption))
    else:
        logging.info('{} sent "{}"'.format(message.from_user.username, message.caption))


def show_error(**kwargs):
    """Logs the error message and the system where the error occurred."""

    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)

    logging.info('{} FAILED: "{}"'.format(kwargs['system'], kwargs['error']))
