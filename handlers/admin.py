from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from borukva_bot import *
from item import *
from shop import *


def check_admin_decorator(func):
    async def inner(msg: types.Message):
        if is_admin(str(msg.from_user.id)):
            await func(msg)
    return inner

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
    if ';' in msg.text:
        msg.reply('";" Не можна використовувати у назві')
        return
    
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
        item.insert()
    await state.finish()

async def cancel_handler(msg: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await msg.reply('Добре, скасовано.')

@check_admin_decorator
async def all_handler(msg: types.Message):
    all_items = Item.all()
    await msg.reply(str(all_items))

@check_admin_decorator
async def remove_item_handler(msg: types.Message):
    try:
        arg = msg.text.split(' ')[-1]
        if arg.isnumeric():
            code = int(msg.text.split(' ')[-1])
            Item.delete(code)
        else:
            text = msg.text.split(' ')[1:]
            text = ' '.join(text)
            item = Item.find_by_name(text, 0.7)
            if item:
                Item.delete(item.code)
        await msg.reply('Предмет видалено!')
        Item.sort()
    except:
        await msg.reply('Не вдалося видалити предмет')

# хендлери адмінів
@check_admin_decorator
async def all_admins_handler(msg: types.Message):
    admins_list = get_all_admins()
    await msg.reply(str(admins_list))

@check_admin_decorator
async def add_admin_handler(msg: types.Message):
    args = msg.text.split(' ')
    insert_admin(args[-2], args[-1])
    await msg.reply(f"Доданий адмін на ім'я: {args[-1]}, з айді: {args[-2]}")

@check_admin_decorator
async def remove_admin_handler(msg: types.Message):
    args = msg.text.split(' ')
    delete_admin(args[-1])
    await msg.reply("Адмін видалений!")

# хендлери магазинів
@check_admin_decorator
async def all_shops_handler(msg: types.Message):
    shops_list = Shop.all()
    await msg.reply(str(shops_list))

@check_admin_decorator
async def remove_shop_handler(msg: types.Message):
    text = msg.text.split(' ')[1:]
    text = ' '.join(text)

    if text.isnumeric():
        id = int(msg.text.split(' ')[-1])
        Shop.delete(id)
    else:
        shop = Shop.find_by_name(text, 0.9)
        if shop:
            Shop.delete(shop.id)
    await msg.reply('Магазин видалено!')


class ShopCreatingState(StatesGroup):
    name = State()
    owner_id = State()
    owner_name = State()

@check_admin_decorator
async def create_shop_start_handler(msg: types.Message):
    await ShopCreatingState.name.set()
    await msg.reply('Назва магазину?')

async def set_shop_name_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = msg.text
    await ShopCreatingState.next()
    await msg.reply('Айді власника? (айді користувача в тґ)')

async def set_shop_owner_id_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['owner_id'] = msg.text
    await ShopCreatingState.next()
    await msg.reply("Ім'я власника? (ім'я користувача в тґ)")

async def set_shop_owner_name_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['owner_name'] = msg.text
    async with state.proxy() as data:
        owner = Owner(data['owner_id'], data['owner_name'])
        try:
            Shop.create(data['name'], owner.str())
            await msg.reply("Магазин доданий")
        except TypeError:
            await msg.reply("У цього користувача вже є магазин")
            await state.finish()
        except:
            await msg.reply("Щось пішло не так під час створення")
    await state.finish()

# хендлери для списків
class ListState(StatesGroup):
    _class = State()

async def all_lists_handler(msg: types.Message):
    await msg.reply(str(ItemList.all()))

@check_admin_decorator
async def add_item_to_list_handler(msg: types.Message):
    await ListState._class.set()
    await msg.reply('Назва списку?')

async def set_adding_items_to_list_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            if data['_class'].name != '':       # назва введена і знайшлася => вводимо предмети
                if msg.text == '*':
                    await msg.reply('Список був оновлений')
                    await state.finish()
                item_to_add = Item.find_by_name(msg.text)
                if item_to_add:
                    data['_class'].items += ';' + item_to_add.name
                    await msg.reply('Предмет доданий')
                else:
                    await msg.reply('Такого предмета немає')
            if ItemList.find_by_name(data['_class'].name):      # назва введена і шукається
                data['_class'].name = msg.text
                await msg.reply('Вписуйте назви предметів (відправте * для завершення)')
            else:                                              # назва введена, але не знайшлася
                await msg.reply('Такого списку немає')
                await state.finish()
        except:
            await msg.reply('Такого списку немає')
            await state.finish()

@check_admin_decorator
async def create_list_handler(msg: types.Message):
    list_name = msg.text.split(' ')[2:]
    list_name = ' '.join(list_name)

    if len(list_name) < 3:
        await msg.reply('Назва списку повинна бути більше 2 літер')
        return
    
    item_list = ItemList(list_name)
    item_list.insert_to_db()

@check_admin_decorator
async def remove_list_handler(msg: types.Message):
    list_name = msg.text.split(' ')[2:]
    list_name = ' '.join(list_name)

    item_list = ItemList.find_by_name(list_name=list_name, ratio=0.8)
    item_list.delete()

def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(all_lists_handler, Text(equals='списки', ignore_case=True))
    dp.register_message_handler(add_item_to_list_handler, Text(startswith='+список', ignore_case=True))
    dp.register_message_handler(set_adding_items_to_list_handler, state=ListState._class)
    #dp.register_message_handler(remove_item_into_list_handler, Text(startswith='-список', ignore_case=True))
    dp.register_message_handler(create_list_handler, Text(startswith='створити список', ignore_case=True))
    dp.register_message_handler(remove_list_handler, Text(startswith='видалити список', ignore_case=True))

    dp.register_message_handler(create_shop_start_handler, Text(equals='+магазин', ignore_case=True), state=None)
    dp.register_message_handler(set_shop_name_handler, state=ShopCreatingState.name)
    dp.register_message_handler(set_shop_owner_id_handler, state=ShopCreatingState.owner_id)
    dp.register_message_handler(set_shop_owner_name_handler, state=ShopCreatingState.owner_name)
    
    dp.register_message_handler(all_shops_handler, Text(equals='магазини', ignore_case=True))
    dp.register_message_handler(remove_shop_handler, Text(startswith='-магазин', ignore_case=True))

    dp.register_message_handler(all_admins_handler, Text(equals='адміни', ignore_case=True))
    dp.register_message_handler(add_admin_handler, Text(startswith='+адмін', ignore_case=True))
    dp.register_message_handler(remove_admin_handler, Text(startswith='-адмін', ignore_case=True))
    
    dp.register_message_handler(remove_item_handler, Text(startswith='видалити', ignore_case=True))
    dp.register_message_handler(all_handler, Text(equals='все', ignore_case=True))
    #dp.register_message_handler(cancel_handler, state='*', commands='скасувати')
    dp.register_message_handler(cancel_handler, Text(equals='скасувати', ignore_case=True), state='*')

    #dp.register_message_handler(add_item_start_handler, state=None, commands='додати')
    dp.register_message_handler(add_item_start_handler, Text(equals='створити', ignore_case=True), state=None)
    dp.register_message_handler(load_icon_handler, content_types=['photo'], state=ItemState.icon)
    dp.register_message_handler(name_item_handler, state=ItemState.name)
    dp.register_message_handler(set_amount_handler, state=ItemState.amount)
    dp.register_message_handler(set_min_price_handler, state=ItemState.min_price)
    dp.register_message_handler(set_max_price_handler, state=ItemState.max_price)