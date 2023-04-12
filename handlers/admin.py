from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from borukva_bot import *


def check_admin_decorator(func):
    def inner(msg: types.Message):
        if is_admin(str(msg.from_id)):
            return func(msg)
        return do_nothing_handler
    return inner

async def do_nothing_handler(msg: types.Message):
    pass

# хендлери предметів
class ItemState(StatesGroup):
    icon = State()
    name = State()
    amount = State()
    min_price = State()
    max_price = State()

@check_admin_decorator
async def add_item_start_handler(msg: types.Message):
    await ItemState.icon.set()
    await msg.reply('Завантажте зображення (зі стисненням)')

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

@check_admin_decorator
async def all_handler(msg: types.Message):
    l = get_all_items()
    await msg.reply(str(l))

@check_admin_decorator
async def remove_item_handler(msg: types.Message):
    try:
        arg = msg.text.split(' ')[-1]
        if arg.isnumeric():
            code = int(msg.text.split(' ')[-1])
            delete_item(code)
        else:
            item = Item.find_by_name(arg, 0.7)
            if item:
                delete_item(item.code)
        await msg.reply('Видалено!')
        sort_items()
    except:
        await msg.reply('Не вдалося видалити предмет')

# хендлери адмінів

async def all_admins_handler(msg: types.Message):
    l = get_all_admins()
    await msg.reply(str(l))

@check_admin_decorator
async def add_admin_handler(msg: types.Message):
    print(msg.text)
    args = msg.text.split(' ')
    insert_admin(args[-2], args[-1])
    await msg.reply(f"Доданий адмін на ім'я: {args[-1]}, з айді: {args[-2]}")

def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(all_admins_handler, Text(equals='адміни', ignore_case=True))
    dp.register_message_handler(add_admin_handler, Text(startswith='новий адмін', ignore_case=True))
    
    dp.register_message_handler(remove_item_handler, Text(startswith='видалити', ignore_case=True))
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