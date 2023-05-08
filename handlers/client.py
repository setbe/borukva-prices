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

async def help(msg: types.Message):
    await msg.answer('''
[назва предмету] — пошук предмета.
магазин [назва] — пошук магазина.

фідбек [повідомлення] — повідомлення до бригади спавну.
(ви отримаєте відповідь в приватних повідомленнях від бота, якщо починали розмову з ним там)
    ''')
    await msg.answer('''
Адмін-команди (ви адмін, ви бачите це повідомленння):

списки — всі списки (не списки предметів у магазинах).
+список — додавати предмети до списку.
-список — вилучати предмети зі списку.
створити список — новий список.
видалити список — видалити існуючий список.

магазини — всі магазини.
+магазин — створити магазин.
-магазин — видалити магазин.

все — всі існуючі предмети в базі даних.
створити — додати предмет в базу даних.
видалити — видалити предмет з бази даних.

скасувати — скасувати якусь дію (наприклад, коли створюєш магазин і вписуєш інформацію до нього — можна скасувати)

фідбеки — список фідбеків
відповісти на [id фідбека] [повідомлення] — відповісти на якийсь фідбек

адміни — список адмінів
+адмін [id] [будь_яке_ім'я] — додати адміна
-адмін [id] — вилучити адміна
        ''')

def register_client_handlers(dp: Dispatcher):

    dp.register_message_handler(help, Text(equals='допомога', ignore_case=True))
    dp.register_message_handler(help, commands='допомога')

    dp.register_message_handler(find_shop, Text(startswith='магазин', ignore_case=True))
    dp.register_message_handler(find_item)