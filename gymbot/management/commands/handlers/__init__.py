from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart

from .text_handler import *


def setup(dp: Dispatcher):
    dp.register_message_handler(start_handler, CommandStart(), state='*')
    dp.register_message_handler(message_handler)
    # dp.register_callback_query_handler(quiz_callback, lambda c: len(c.data.split('_')) == 2)
    ...
