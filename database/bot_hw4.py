import sqlite3
from config import bot
import random

def sql_create():
    global db, cursor
    db = sqlite3.connect("bot5.sqlite3")
    cursor = db.cursor()
    if db:
        print("База данных подключена!")
    db.execute("CREATE TABLE IF NOT EXISTS users"
               "(photo TEXT, name TEXT, description TEXT, "
               "price INTEGER)")
    db.commit()

async def sql_command_insert(state):
    async with state.proxy() as data:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)", tuple(data.values()))
        db.commit()

async def sql_command_random(message):
    result = cursor.execute("SELECT * FROM users").fetchall()
    r_d = random.randint(0, len(result)-1)
    await bot.send_photo(message.from_user.id, result[r_d][0],
                         caption=f"Name: {result[r_d][1]}\n"
                                 f"Description: {result[r_d][2]}\n"
                                 f"Price: {result[r_d][3]}")

async def sql_command_all(message):
    return cursor.execute("SELECT * FROM users").fetchall()

async def sql_command_delete(name):
    cursor.execute("DELETE FROM users WHERE name == ?", (name,))
    db.commit()



