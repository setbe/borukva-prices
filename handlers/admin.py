from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

class ItemAdmin(StatesGroup):
    icon = State()
    name = State()
    amount = State()
    min_price = State()
    max_price = State()

async def add_item_start(msg: types.Message):
    await ItemAdmin.icon.set()
    await msg.reply('Завантажте зображення.')

async def load_icon(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['icon'] = msg.photo[0].file_id
    await ItemAdmin.next()
    await msg.reply('Назва?')

async def name_item(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = msg.text
    await ItemAdmin.next()
    await msg.reply('Кількість товару?')

async def set_amount(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = msg.text
    await ItemAdmin.next()
    await msg.reply('Мінімальна ціна?')

async def set_min_price(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['min_price'] = int(msg.text)
    await ItemAdmin.next()
    await msg.reply('Максимальна ціна?')

async def set_max_price(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['max_price'] = int(msg.text)
    async with state.proxy() as data:
        await msg.reply(str(data))
    await state.finish()

async def cancel_handler(msg: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await msg.reply('Добре, скасовано.')

def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(cancel_handler, state='*', commands='скасувати')
    dp.register_message_handler(cancel_handler, Text(equals='скасувати', ignore_case=True), state='*')
    dp.register_message_handler(add_item_start, state=None, commands='додати')
    dp.register_message_handler(add_item_start, Text(equals='додати', ignore_case=True), state=None)
    dp.register_message_handler(load_icon, content_types=['photo'], state=ItemAdmin.icon)
    dp.register_message_handler(name_item, state=ItemAdmin.name)
    dp.register_message_handler(set_amount, state=ItemAdmin.amount)
    dp.register_message_handler(set_min_price, state=ItemAdmin.min_price)
    dp.register_message_handler(set_max_price, state=ItemAdmin.max_price)