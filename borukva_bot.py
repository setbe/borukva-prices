from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram import types

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from key import token
from data import *

fsm_storage = MemoryStorage()

bot = Bot(token=token)
dp = Dispatcher(bot=bot, storage=fsm_storage)