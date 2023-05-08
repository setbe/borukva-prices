from data import *

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
            self.code = len(Item.all())
    
    def info(self):
        return f'''
Кількість: {self.amount}
Назва: {self.name}
Мін. ціна: {rg_to_rbg(self.min_price)}
Макс. ціна: {rg_to_rbg(self.max_price)}
Код товару: {str(self.code)}   
'''

    def insert(self):
        with con:
            cur.execute('INSERT INTO items VALUES (?, ?, ?, ?, ?, ?)', (self.icon, self.name, self.amount, self.min_price, self.max_price, self.code, ))

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

    @classmethod
    def find_by_name(cls, item_name: str, ratio = 0.3):
        names = Item.names()
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

            item = Item.by_name(item[0])

            if item: 
                return item
        return None
    
    @classmethod
    def sort(cls):
        items = Item.all()
        for item in items:
            Item.delete(item[5])
        for item in items:
            new_code_item = Item(item[0], item[1], item[2], item[3], item[4])
            new_code_item.insert()

    @classmethod
    def delete(cls, code: int):
        with con:
            cur.execute('DELETE from items where code=?', (code, ))

    @classmethod
    def by_code(cls, code: int):
        with con:
            cur.execute('SELECT * from items where code=?', (code, ))
        return Item.from_data(cur.fetchone())
    
    @classmethod
    def all(cls):
        with con:
            cur.execute('SELECT * from items')
        return cur.fetchall()
    
    @classmethod
    def names(cls):
        with con:
            cur.execute('SELECT name from items')
        return cur.fetchall()

    @classmethod
    def by_name(cls, name: str):
        with con:
            cur.execute('SELECT * from items where name=?', (name, ))
        return Item.from_data(cur.fetchone())
    
class ItemList():
    def __init__(self, name='', items='') -> None:
        self.name = name
        self.items = items

    def insert_to_db(self):
        with con:
            cur.execute('INSERT INTO lists VALUES (?, ?)', (self.name, self.items))

    def delete(self):
        with con:
            cur.execute('DELETE * FROM lists WHERE name=?', (self.name))

    @classmethod
    def from_data(cls, data):
        item_list = ItemList()
        item_list.name = data['name']
        item_list.items = data['items']
        return item_list
    
    @classmethod
    def all(cls):
        with con:
            cur.execute('SELECT * FROM lists')
        return cur.fetchall()
    
    @classmethod
    def names(cls):
        with con:
            cur.execute('SELECT name FROM lists')
        return cur.fetchall()

    @classmethod
    def find_by_name(cls, list_name: str, ratio = 0.3):
        names = ItemList.names()
        results = []
        for name in names:
            res = similar(name[0], list_name, ratio=ratio)
            if res:
                results.append(res)
        
        if len(results) > 0:    # not empty
            item = results[0]

            for res in results:
                if res[2] > item[2]:    # compare ratios
                    item = res

            item = ItemList.by_name(item[0])

            if item: 
                return item
        return None
    
    @classmethod
    def by_name(cls, list_name: str):
        with con:
            cur.execute('SELECT * FROM lists WHERE name=?', (list_name, ))
        return ItemList.from_data(cur.fetchone())
    
    @classmethod
    def add_item(cls, list_name: str, item: str):
        item_list = ItemList.find_by_name(list_name)
        item_to_add = Item.find_by_name(item).name

        items = item_list.items.split(' ')
        if item_to_add in items:
            items.append(item_to_add)
        items = ' '.join(items)
        with con:
            cur.execute('UPDATE lists SET items=? WHERE name=?', (items, item_list.name))
    
    @classmethod
    def delete_item(cls, list_name: str, item: str):
        item_list = ItemList.find_by_name(list_name)
        item_to_delete = Item.find_by_name(item).name

        items = item_list.items.split(' ')
        items.remove(item_to_delete)
        items = ' '.join(items)
        with con:
            cur.execute('UPDATE lists SET items=? WHERE name=?', (items, item_list.name))