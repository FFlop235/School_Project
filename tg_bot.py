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
btn_continue = InlineKeyboardButton('Продолжить', callback_data='continue1')
btn_yes = InlineKeyboardButton('Да', callback_data='yes')
btn_no = InlineKeyboardButton('Нет', callback_data='no')

kb_yes_or_no = InlineKeyboardMarkup().add(btn_yes).add(btn_no)
kb_start = InlineKeyboardMarkup().add(btn_reg).add(btn_continue)
kb_continue_to_main_menu = InlineKeyboardMarkup().add(btn_continue)
kb_reg = InlineKeyboardMarkup().add(btn_reg)

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Этот бот был создан для наглядной демонстрации изменения оценок, по тому или иному предмету. \n", reply_markup=kb_start)

@dp.callback_query_handler(text=['continue1'])
async def call_main_menu(call: types.CallbackQuery):
    await call.message.delete()
    user_id = call.from_user.id
    id_list = select_id()
    if str(user_id) in id_list:
        await call.message.answer('Добрый день. Если хотите выстроить график нажмите кнопку "Продолжить" ниже.')
    else:
        await call.message.answer('Извините, но вы не зарегестрированы. Нажмите на кнопку "Зарегистрироватся" ниже', reply_markup=kb_reg)

@dp.callback_query_handler(text=['reg'])
async def call_continue(call: types.CallbackQuery):
    await call.message.delete()
    user_id = call.from_user.id
    id_list = select_id()
    if str(user_id) in id_list:
        await call.message.answer("Вы уже зарегестрированы!", reply_markup=kb_continue_to_main_menu)
    else:
        await call.message.answer("Напишите ваш логин из сетевого города ниже: ")
        await UserState.login.set()

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
                         f"Пароль {data['password']}\n"
                         "Всё верно?", reply_markup=kb_yes_or_no)
    
    # create_user_data(message.from_user.id, str(data['login']), str(data['password']))
    # save_changes()

    await state.reset_state(with_data=False)

@dp.callback_query_handler(text='yes')
async def call_yes(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    create_user_data(call.from_user.id, str(data['login']), str(data['password']))
    save_changes()

    await state.finish()

@dp.callback_query_handler(text='no')
async def call_yes(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Что бы изменить данные, нажмите кнопку 'Зарегистрироватся' ниже", reply_markup=kb_reg)

    await state.finish()




if __name__ == '__main__':
    executor.start_polling(dp)