from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from borukva_bot import *

from handlers import client, admin

client.register_client_handlers(dp)
admin.register_admin_handlers(dp)


executor.start_polling(dp, skip_updates=True)