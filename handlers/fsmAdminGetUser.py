from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from .keyboards import cancel_markup
from config import bot
from database import bot_db

# States

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    surname = State()
    age = State()
    region = State()

async def fsm_start(message: types.Message):
    await FSMAdmin.photo.set()
    await bot.send_message(message.chat.id, f'Hi !{message.from_user.full_name}, send picture...',reply_markup=cancel_markup)

# load photo
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data['nickname']=  f'@{message.from_user.username}'
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, f'Whats u name ?')

# load_name
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, f'Whats u surname ?')

async def load_surname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, f'Whats u age ?')

async def load_age(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['age'] = int(message.text)
        await FSMAdmin.next()
        await bot.send_message(message.chat.id, f'Где живешь ?   ')
    except:
        await bot.send_message(message.chat.id, f'Пиши только цифрами  ! ')


async def load_region(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['region'] = message.text
    # async with state.proxy() as data:
    #     await bot.send_message(message.chat.id, str(data))
    await bot_db.sql_command_insert(state)
    
    await state.finish()
    await bot.send_message(message.chat.id, f'Все свободен!')

async def cancel_reg(message:types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.finish()
        await message.reply('OK')


def register_handler_fsmAdminGetUser(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, state = "*", commands='cancel')
    dp.register_message_handler(cancel_reg, Text(equals='cancel', ignore_case=True),state = '*')

    dp.register_message_handler(fsm_start, commands=['reg'])
    dp.register_message_handler(load_photo, state=FSMAdmin.photo, content_types=['photo'])
    dp.register_message_handler(load_name, state = FSMAdmin.name)
    dp.register_message_handler(load_surname, state =FSMAdmin.surname)
    dp.register_message_handler(load_age, state =FSMAdmin.age)
    dp.register_message_handler(load_region, state =FSMAdmin.region)


    

    


