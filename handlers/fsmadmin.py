from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards import admin_kb
from config import bot
from database import bot_db

class FSMADMIN(StatesGroup):
    photo = State()
    title = State()
    description = State()

async def is_admin_command(message: types.Message):
    global ADMIN_ID
    ADMIN_ID = message.from_user.id
    # "777097353"в виде константа
    # print(ADMIN_ID)
    await bot.send_message(message.from_user.id,
                           "'Yes, admin\n"
                           "what do you need",
                           reply_markup=admin_kb.button_admin)
    await message.delete()

async def cancel_command(message: types.Message,
                         state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        current_state = await state.get_state()
        if current_state is None:
            return "State is None, Relax"
        await state.finish()
        await message.reply("Canceled")

async def fsm_start(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await FSMADMIN.photo.set()
        await message.reply("Admin, send me photo please")

async def load_photo(message: types.Message,
                     state: FSMContext):
    # if message.from_user.id == ADMIN_ID:
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMADMIN.next()
    await message.reply("Admin, Send me titile of photo")

async def load_title(message: types.Message,
                     state: FSMContext):
    # if message.from_user.id == ADMIN_ID:
    async with state.proxy() as data:
        data['titile'] = message.text
    await FSMADMIN.next()
    await message.reply("Admin, send me description of photo")

async def load_description(message: types.Message,
                           state: FSMContext):
    # if message.from_user.id == ADMIN_ID:
    async with state.proxy() as data:
        data['description'] = message.text
        # async with state.proxy() as data:
        #     await message.reply(str(data))
    await bot_db.sql_insert(state)
    await state.finish()

async def complete_delete(call: types.CallbackQuery):
    await bot_db.sql_delete(call.data.replace("delete", ""))
    await call.answer(text=f'{call.data.replace("delete", "")} deleted',
                      show_alert=True)

async def delete_data(message: types.Message):
    selected_data = await bot_db.sql_casual_select()
    for result in selected_data:
        await bot.send_photo(
            message.chat.id,
            result[0],
            caption=f'Title: {result[1]}\n Description: {result[2]}',
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    f'delete: {result[1]}',
                    callback_data=f'delete {result[1]}'
                )
            )
        )

def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(is_admin_command, commands=['admin'])
    dp.register_message_handler(cancel_command, state='*', commands=['cancel'])
    dp.message_handler(cancel_command, Text(equals='cancel', ignore_case=False), state='*')
    dp.register_message_handler(fsm_start, commands=['upload'], state=None)
    dp.register_message_handler(load_photo,
                                content_types=['photo'], state=FSMADMIN.photo)
    dp.register_message_handler(load_title, state=FSMADMIN.title)
    dp.register_message_handler(load_description, state=FSMADMIN.description)
    dp.register_callback_query_handler(
        complete_delete,
        lambda call: call.data and call.data.startwish("delete"))
    dp.register_message_handler(delete_data, commands=['delete'])