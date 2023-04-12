import sqlite3, math
from difflib import SequenceMatcher

def similar(original, to_compare, ratio = 0.8):
    ratio_match = SequenceMatcher(None, original, to_compare).ratio()
    if ratio_match >= ratio:
        return (original, to_compare, ratio_match)
    else:
        return None
    
# converts raw gold to raw block of gold (string)
def rg_to_rbg(num: int):
    if num > 128:
        rbg = math.floor(num / 9)
        if num % 9 != 0:
            return f'{str(rbg)} БНЗ + {num % 9} НЗ'
        else:
            return f'{str(rbg)} БНЗ'
    else:
        return str(num) + ' НЗ'
    
    
class Item():
    def __init__(self, icon = '', name = '', amount = 0, min = 0, max = 0, code = None) -> None:
        self.icon = icon
        self.name = name
        self.amount = amount
        self.min_price = min
        self.max_price = max
        if code:
            self.code = code
        else:
            self.code = len(get_all_items())

    @classmethod
    def from_data(cls, data: list):
        item = Item()
        item.icon = data[0]
        item.name = data[1]
        item.amount = data[2]
        item.min_price = data[3]
        item.max_price = data[4]
        item.code = data[5]
        return item
    
    def info(self):
        return f'''
Кількість: {self.amount}
Назва: {self.name}
Мін. ціна: {rg_to_rbg(self.min_price)}
Макс. ціна: {rg_to_rbg(self.max_price)}
Код товару: {str(self.code)}   
'''

    @classmethod
    def find_by_name(cls, item_name: str, ratio = 0.3):
        names = get_items_names()
        results = []
        for name in names:
            res = similar(name[0], item_name, ratio=ratio)
            if res:
                results.append(res)
        
        if len(results) > 0:    # not empty
            item = results[0]

            for res in results:
                if res[2] > item[2]:    # compare ratios
                    item = res

            item = get_item_by_name(item[0])
            item = Item(item[0], item[1], item[2], item[3], item[4], item[5])

            if item: 
                return item
        return None
        
class Shop():
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description
        self.items = []

con = sqlite3.connect('data.db')
cur = con.cursor()

# cur.execute('''CREATE TABLE items (
#                 icon text,
#                 name text,
#                 amount integer,
#                 min integer,
#                 max integer,
#                 code integer
# )''')


# cur.execute('''CREATE TABLE admins (
#                 id text,
#                 name text
# )''')

# cur.execute('''CREATE TABLE shops (
#                 icon text,
#                 name text,
#                 description text,
#                 owners text,
#                 items text,
#                 id integer
# )''')


# операції з товарами
def sort_items():
    items = get_all_items()
    for item in items:
        delete_item(item[5])
    for item in items:
        new_code_item = Item(item[0], item[1], item[2], item[3], item[4])
        insert_item(new_code_item)

def insert_item(item: Item):
    with con:
        cur.execute('INSERT INTO items VALUES (?, ?, ?, ?, ?, ?)', (item.icon, item.name, item.amount, item.min_price, item.max_price, item.code, ))

def delete_item(code: int):
    with con:
        cur.execute('DELETE from items where code=?', (code, ))

def get_item(code: int):
    with con:
        cur.execute('SELECT * from items where code=?', (code, ))
    return Item.from_data(cur.fetchone())

def get_all_items():
    with con:
        cur.execute('SELECT * from items')
    return cur.fetchall()

def get_items_names():
    with con:
        cur.execute('SELECT name from items')
    return cur.fetchall()

def get_item_by_name(name: str):
    with con:
        cur.execute('SELECT * from items where name=?', (name, ))
    return cur.fetchone()



# операції з адмінами
def get_all_admins():
    with con:
        cur.execute('SELECT * from admins')
    return cur.fetchall()

def insert_admin(id: str, name: str):
    with con:
        cur.execute('INSERT INTO admins VALUES (?, ?)', (id, name, ))

def delete_admin(id: str):
    with con:
        cur.execute('DELETE from admins where id=?', (id, ))
    
def get_admin_id(name: str):
    with con:
        cur.execute('SELECT id from admins where name=?', (name, ))
    return cur.fetchone()

def is_admin(id: str):
    with con:
        cur.execute('SELECT * from admins where id=?', (id))
    return cur.fetchone()


# операції з магазинами
def get_all_shops():
    with con:
        cur.execute('SELECT * from shops')
    return cur.fetchall()

def create_shop(owners: str):
    id = len(get_all_shops())
    with con:
        cur.execute('INSERT INTO shops VALUES (?, ?, ?, ?, ?, ?)', ('', 'Без назви', f'Якось тут порожньо...\nредагувати {str(id)} - для встановлення інформації.', owners, '{}', id, ))

def insert_shop(icon: str, name: str, description: str, id: int):
    with con:
        cur.execute("UPDATE shops SET icon=?, name=?, description=? WHERE id=?", (icon, name, description, id))

def delete_shop(id: int):
    with con:
        cur.execute('DELETE from shops where id=?', (id, ))

def find_shop(name: str):
    pass