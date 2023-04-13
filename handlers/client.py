from borukva_bot import *
from aiogram.dispatcher.filters import Text
from item import *
from shop import *
from aiogram.utils.exceptions import BadRequest

async def find_item(msg: types.Message):
    item = Item.find_by_name(msg.text)
    if item:
        await msg.reply_photo(photo=item.icon, caption=item.info())

async def find_shop(msg: types.Message):
    text = msg.text.split(' ')[1:]
    text = ' '.join(text)
    shop = Shop.find_by_name(text)
    if shop:
        try:
            await msg.reply_photo(photo=shop.icon, caption=shop.info())
        except BadRequest:
            await msg.reply(shop.info())

def register_client_handlers(dp: Dispatcher):
    dp.register_message_handler(find_shop, Text(startswith='магазин', ignore_case=True))

    dp.register_message_handler(find_item)