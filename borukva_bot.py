from difflib import SequenceMatcher
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram import types

from aiogram.contrib.fsm_storage.files import JSONStorage

from key import token

fsm_storage = JSONStorage('fsm.db')

bot = Bot(token=token)
dp = Dispatcher(bot=bot, storage=fsm_storage)

async def similar(a, b):
    if SequenceMatcher(None, a, b).ratio() >= 0.8:
        return True
    else:
        return False