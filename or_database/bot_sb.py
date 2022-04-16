import random
import sqlite3

from config import bot


def sql_create():
    global dp, cursor
    db = sqlite3.connect('bot.sqlite3')
    cursor = db.cursor()
    if db:
        print('dataBase connect...')
    db.execute("CREATE TABLE IF NOT EXISTS anketa"
               "(id INTEGER PRIMARY KEY, nickname TEXT, photo TEXT" 
               "name TEXT, surname TEXT, age INT, regoin TEXT)")
    dp.commit()

async def sdq_commands_insert(state):
    async with state.proxy() as data:
        cursor.execute('INSERT INTO anketa VALUES (?,?,?,?,?,?,?)', tuple(data.values()))
        dp.commit()

async def sql_command_random(message):
    result = cursor.execute("SELECT * FROM anketa").fetchall()
    r_u = random.randint(0, len(result)-1)
    await bot.send_photo(message.from_user.id, result[r_u][2], 
                        caption=f'Name: {result[r_u][3]}\n'
                                                 f'Surname: {result[r_u][4]}\n'
                                                 f'Age: {result[r_u][5]}\n'
                                                 f'Region: {result[r_u][6]}\n\n'
                                                 f'{result[r_u][1]}')


async def sql_command_all(message):
    return cursor.execute("SELECT * FROM anketa").fetchall()


async def sql_command_delete(id):
    cursor.execute('DELETE FROM anketa WHERE id == ?',(id))
    dp.commit()

