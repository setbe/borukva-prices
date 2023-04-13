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
    def get_by_code(cls, code: int):
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