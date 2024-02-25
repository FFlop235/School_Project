from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ContentType
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from DataBase import create_user_data, update_user_data, delete_user_data, select_user_data, select_id, save_changes

import json
import logging

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

bot = Bot(TOKEN)
dp = Dispatcher(bot=bot, storage=storage)

class UserState(StatesGroup):
    login = State()
    password = State()

btn_reg = InlineKeyboardButton('Зарегистрироватся', callback_data='reg')
kb1 = InlineKeyboardMarkup().add(btn_reg)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Этот бот был создан для наглядной демонстрации изменения оценок, по тому или иному предмету. \n", reply_markup=kb1)

@dp.callback_query_handler(text=['reg'])
async def call_continue(call: types.CallbackQuery):
    await call.message.delete()
    if call.from_user.id not in select_id():
        await call.message.answer("Напишите ваш логин из сетевого города ниже: ")
        await UserState.login.set()
    else:
        await call.message.answer("Вы уже зарегестрированы!")

@dp.message_handler(state=UserState.login)
async def get_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("Отлично! Теперь введите пароль от него.")
    await UserState.next()

@dp.message_handler(state=UserState.password)
async def get_password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    await message.answer(f"Логин: {data['login']}\n"
                         f"Пароль {data['password']}")
    
    create_user_data(message.from_user.id, str(data['login']), str(data['password']))
    save_changes()

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp)