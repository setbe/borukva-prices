from borukva_bot import *
from aiogram.dispatcher.filters import Text

async def echo_send(msg: types.Message):
    item = Item.find_by_name(msg.text)
    if item:
        await msg.reply_photo(photo=item.icon, caption=item.info())

def register_client_handlers(dp: Dispatcher):
    dp.register_message_handler(echo_send)