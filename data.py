import sqlite3

class Item():
    def __init__(self, icon = '', name = '', amount = 0, min = 0, max = 0) -> None:
        self.icon = icon
        self.name = name
        self.amount = amount
        self.min_price = min
        self.max_price = max
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
#                 id text
# )''')

# cur.execute('''CREATE TABLE shops (
#                 icon text,
#                 name text,
#                 description text,
#                 owners text,
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



# операції з адмінами
def get_all_admins():
    with con:
        cur.execute('SELECT * admins')
    return cur.fetchall()


# операції з магазинами