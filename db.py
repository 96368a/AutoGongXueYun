import sqlite3
import json

sqlite3.register_adapter(dict, json.dumps)
sqlite3.register_adapter(list, json.dumps)
sqlite3.register_converter("JSON", json.loads)

db = sqlite3.connect('db/data.sqlite',detect_types=sqlite3.PARSE_DECLTYPES,check_same_thread=False)

def init_db():
    db.execute('CREATE TABLE IF NOT EXISTS users (phone integer PRIMARY KEY, data Json)')
    db.commit()

def insert(data):
    db.execute('INSERT INTO users (data) VALUES (?)', (data,))
    
def getOneByPhone(phone):
    user = db.execute('SELECT data FROM users WHERE phone = ?', (phone,)).fetchone()
    if user:
        return user[0]
    return None
    
def get_all():
    return db.execute('SELECT data FROM users').fetchall()

def insert(data):
    db.execute('INSERT INTO users (phone,data) VALUES (?,?)', (data['phone'],data))
    db.commit()    

def test():
    db.execute('INSERT INTO users (phone,data) VALUES (?,?)', (18888888888,{'name': 'John', 'age': 25}))
    db.execute('INSERT INTO users (phone,data) VALUES (?,?)', (17777777777,{'name': 'John', 'age': 26}))
    db.commit()
    
if __name__ == '__main__':
    init_db()
    # test()
    # user = getOneByPhone(18888888888)
    # print(user)
    # users = list(map(lambda x: x[0],get_all()))
    # print(users)
    with open('user.json','r',encoding='utf-8') as f:
        datas = json.load(f)
        insert(datas[0])
