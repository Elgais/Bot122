from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot

class FSMAdmin(StatesGroup):
    obl = State()
    title = State()
    describe = State()
    price = State()

async def dow_start(message: types.Message):
    await FSMAdmin.obl.set()
    await bot.send_message(message.chat.id, f'Good Morning ! {message.from_user.full_name},send picture... ')


async def dow_pic(message: types.Message, state: FSMContext):
    async with state.proxy() as menu:
        menu['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, f'Title ?')


async def dow_tit(message: types.Message, state: FSMContext):
    async with state.proxy() as menu:
        menu['title'] = message.text
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, 'Describe you meal...')

async def dow_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as menu:
        menu['desc'] = message.text
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, ' Price ?')
        

async def dow_price(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as menu:
            menu['price'] = int(message.text)
        await state.finish()
        await bot.send_message('Thank u , good day!')
    except:
        await bot.send_message(message.chat.id, 'Only with int !')


async def cancel_reg(message:types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.finish()
        await message.reply('See u next time !')

def register_handler_fsmAdminMenu(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, state = "*", commands='cancel')
    dp.register_message_handler(cancel_reg, Text(equals='cancel', ignore_case=True),state = '*')
    dp.register_message_handler(dow_start, commands=['exala'])
    dp.register_message_handler(dow_pic, state= FSMAdmin.obl, content_types=['photo'])
    dp.register_message_handler(dow_tit, state= FSMAdmin.title)
    dp.register_message_handler(dow_desc, state= FSMAdmin.describe)
    dp.register_message_handler(dow_price, state= FSMAdmin.price)


