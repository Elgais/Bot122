from aiogram import executor
from config import dp
import logging
from handlers import client, callback, notification, fsmAdminGetUser, fsmAdminMenu, get_menu_update
from database import bot_hw4

async def on_start_up(_):
    bot_hw4.sql_create()


client.register_hendlers_client(dp)
callback.register_hendlers_callback(dp)
get_menu_update.register_hendler_get_menu_update(dp)
# fsmAdminMenu.register_handler_fsmAdminMenu(dp)
# fsmAdminGetUser.register_hendler_fsmAdminGetUser(dp)
notification.register_hendlers_notification(dp)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=False, on_startup=on_start_up)







