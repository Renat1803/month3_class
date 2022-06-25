from aiogram.utils import executor
from config import bot, dp
from handlers import client, callback, extra, fsmadmin, notification
from database import bot_db
import asyncio

async def on_startup(_):
    bot_db.sql_create()
    asyncio.create_task(notification.scheduler())
    print(" bot is online")

client.register_handlers_client(dp)
fsmadmin.register_handler_admin(dp)
callback.register_handlers_callback(dp)
notification.register_handler_notification(dp)
extra.register_handlers_other(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

