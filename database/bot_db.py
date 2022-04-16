import sqlite3
from config import bot

def sql_create():
    global dp, cursor
    db = sqlite3.connect('bot.sqlite3')
    cursor = db.cursor()
    if db :
        print('DataBase connect...')
    db.execute("CREATE TABLE IF NOT EXISTS anketa"
               "(id INTEGER PRIMARY KEY, nickname TEXT, photo TEXT" 
               "name TEXT, surname TEXT, age INT, regoin TEXT)")
    dp.commit()



