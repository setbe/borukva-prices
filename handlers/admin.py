from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from borukva_bot import get_all_items, insert_item, delete_item, Item, get_item, sort_items

class ItemState(StatesGroup):
    icon = State()
    name = State()
    amount = State()
    min_price = State()
    max_price = State()

async def add_item_start_handler(msg: types.Message):
    await ItemState.icon.set()
    await msg.reply('Завантажте зображення.')

async def load_icon_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['icon'] = msg.photo[0].file_id
    await ItemState.next()
    await msg.reply('Назва?')

async def name_item_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = msg.text
    await ItemState.next()
    await msg.reply('Кількість товару?')

async def set_amount_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = msg.text
    await ItemState.next()
    await msg.reply('Мінімальна ціна?')

async def set_min_price_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['min_price'] = int(msg.text)
    await ItemState.next()
    await msg.reply('Максимальна ціна?')

async def set_max_price_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['max_price'] = int(msg.text)
    async with state.proxy() as data:
        item = Item(data['icon'], data['name'], data['amount'], data['min_price'], data['max_price'])
        insert_item(item)
    await state.finish()

async def cancel_handler(msg: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await msg.reply('Добре, скасовано.')

async def all_handler(msg: types.Message):
    l = get_all_items()
    await msg.reply(str(l))

async def remove_item_handler(msg: types.Message):
    try:
        code = int(msg.text.split(' ')[-1])
        delete_item(code)
        await msg.reply('Видалено!')
        sort_items()
    except ValueError:
        await msg.reply('Після "Видалити" треба писати код товару! (код це число)')

async def get_item_handler(msg: types.Message):
    try:
        code = int(msg.text.split(' ')[-1])
        item = get_item(code)
        await msg.reply_photo(item.icon, caption=f'{item.amount} - "{item.name}". Мін-макс. ціна: {item.min_price}-{item.max_price}')
    except ValueError:
        await msg.reply('Після "Товар" треба писати код товару! (код це число)')


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(remove_item_handler, Text(startswith='видалити', ignore_case=True))

    dp.register_message_handler(get_item_handler, Text(startswith='товар', ignore_case=True))
    
    dp.register_message_handler(all_handler, Text(equals='все', ignore_case=True))

    dp.register_message_handler(cancel_handler, state='*', commands='скасувати')
    dp.register_message_handler(cancel_handler, Text(equals='скасувати', ignore_case=True), state='*')

    dp.register_message_handler(add_item_start_handler, state=None, commands='додати')
    dp.register_message_handler(add_item_start_handler, Text(equals='додати', ignore_case=True), state=None)
    dp.register_message_handler(load_icon_handler, content_types=['photo'], state=ItemState.icon)
    dp.register_message_handler(name_item_handler, state=ItemState.name)
    dp.register_message_handler(set_amount_handler, state=ItemState.amount)
    dp.register_message_handler(set_min_price_handler, state=ItemState.min_price)
    dp.register_message_handler(set_max_price_handler, state=ItemState.max_price)