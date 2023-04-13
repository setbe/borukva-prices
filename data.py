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
    
def text_to_price(text: str):
    pass

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

def is_admin(id: str):
    with con:
        cur.execute('SELECT * from admins where id=?', (id, ))
    admin = cur.fetchone()
    if admin:
        if admin[0] == id:
            return True
    return False