from data import *

class Shop():
    def __init__(self, icon='', name='', description='', owners='', items='', id=None) -> None:
        self.icon = icon
        self.name = name
        self.description = description
        self.owners = owners
        self.items = items

        if id:
            self.id = id
        else:
            self.id = Shop.generate_id()

    @classmethod
    def from_data(cls, data: list):
        shop = Shop()
        shop.icon = data[0]
        shop.name = data[1]
        shop.description = data[2]
        shop.owners = data[3]
        shop.items = data[4]
        shop.id = data[5]
        return shop

    def update(self, icon: str, name: str, description: str):
        with con:
            cur.execute("UPDATE shops SET icon=?, name=?, description=? WHERE id=?", (icon, name, description, id))

    @classmethod
    def generate_id(cls):
        with con:
            cur.execute('SELECT id FROM shops')
        shops = cur.fetchall()
        if not shops:
            return 0
        j = 0
        for i in range(len(shops)):
            if j != i:
                return j
            j += 1
        return len(Shop.names())

    @classmethod
    def all(cls):
        with con:
            cur.execute('SELECT * FROM shops')
        return cur.fetchall()

    @classmethod
    def names(cls):
        with con:
            cur.execute('SELECT name FROM shops')
        return cur.fetchall()

    @classmethod
    def create(cls, name: str, owners: str):
        owner = Owner.dict(owners)
        print(owner)
        if Shop.by_user_id(owner['id']):
            raise TypeError
        else:
            id = Shop.generate_id()
            with con:
                cur.execute('INSERT INTO shops VALUES (?, ?, ?, ?, ?, ?)', ('', name, f'''Якось тут порожньо...
редагувати {str(id)} - для встановлення інформації.''', owners, '{}', id, ))

    @classmethod
    def delete(cls, id: int):
        with con:
            cur.execute('DELETE from shops where id=?', (id, ))

    @classmethod
    def by_user_id(cls, id: str):
        res = []
        with con:
            cur.execute('SELECT owners, id FROM shops')
        res = cur.fetchall()
        for i, owner in enumerate(res):
            owner = Owner.dict(owner[0])
            if owner['id'] == id:
                return Shop.by_id(res[i][1]) 
        return None
    
    @classmethod
    def by_id(cls, id: int):
        with con:
            cur.execute('SELECT * FROM shops WHERE id=?', (id, ))
        return cur.fetchone()

    @classmethod
    def by_name(cls, name: str):
        with con:
            cur.execute('SELECT * FROM shops where name=?', (name, ))
        return Shop.from_data(cur.fetchone())

    @classmethod
    def find_by_name(cls, shop_name: str, ratio = 0.3):
        names = Shop.names()
        results = []
        for name in names:
            res = similar(name[0], shop_name, ratio=ratio)
            if res:
                results.append(res)
        
        if len(results) > 0:    # not empty
            shop = results[0]

            for res in results:
                if res[2] > shop[2]:    # compare ratios
                    shop = res

            shop = Shop.by_name(shop[0])

            if shop: 
                return shop
        return None
    
    def info(self):
        return f'''
"{self.name}"

Опис: {self.description}

Власник: {Owner.dict(self.owners)['name']}
Айді магазину: {self.id}
'''


class Owner():
    def __init__(self, id='', name=''):
        self.id = id
        self.name = name
    
    def str(self):
        return str({'id': self.id, 'name': self.name})
    
    @classmethod
    def dict(cls, string) -> dict:
        return eval(string)
