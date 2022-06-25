from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from keyboards import client_kb
from config import bot
from database import bot_db
from parser import scrapy

async def hello(message: types.Message):
    await message.reply(text="hello my boss",
                        reply_markup=client_kb.start_markup)

async def help(message: types.Message):
    await message.reply(text="1. /quiz will start quiz\n"
                             "Следуйщая викторина this is next quiz\n"
                             "Note: Admin_bot will delete cursed words, so that s why you need to be careful ")
    # await bot.ban_chat_member()

async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton("Следуйщая викторина",
                                         callback_data="button_call_1")
    markup.add(button_call_1)
    question = "how old is Putin"
    answers = [
        "50+","60+","70+","immortal"
    ]
    await bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=3,
        explanation="Becuase Putin is immortal",
        explanation_parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=markup,
    )

async def get_all_tvshow(message: types.Message):
    await bot_db.sql_select(message)

async def parser_online(message: types.Message):
    data = scrapy.scrapy_script()
    await bot.send_message(message.chat.id, data)

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(hello, commands=['start'])
    dp.register_message_handler(help, commands=['help'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_message_handler(get_all_tvshow, commands=['tvshow'])
    dp.register_message_handler(parser_online, commands=['scrapy'])