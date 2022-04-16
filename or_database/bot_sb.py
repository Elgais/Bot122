import sqlite3
from config import bot

def sql_create():
    global dp, cursor
    db = sqlite3.connect('bot.sqlite3')
    cursor = db.cursor()
    if db:
        print('DataBase connect...')
    db.execute("CREATE TABLE IF NOT EXISTS anketa"
               "(id INTEGER PRIMARY KEY, nickname TEXT, photo TEXT" 
               "name TEXT, surname TEXT, age INT, regoin TEXT)")
    dp.commit()

async def sdq_commands_insert(state):
    async with state.proxy() as data:
        cursor.execute('INSERT INTO anketa VALUES (?,?,?,?,?,?,?)', tuple(data.values()))
        dp.commit()



