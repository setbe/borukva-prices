from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from borukva_bot import *

from handlers import client, admin

async def on_startup(_):
    print('bot started')

async def on_shutdown(_):
    print('bot stopped')
    con.close()

admin.register_admin_handlers(dp)
client.register_client_handlers(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)