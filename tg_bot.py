from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ContentType
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputFile 

from DataBase import create_user_data, select_user_data, select_id, save_changes
from sup import CreateFile

from pathlib import Path

import logging

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

bot = Bot(TOKEN)
dp = Dispatcher(bot=bot, storage=storage)

# * Регистриция в Сетевой город

class UserState(StatesGroup):
    login = State()
    password = State()

class SubjectState(StatesGroup):
    Subject = State()
    Quarter = State()

# * Кнопочки

btn_reg = InlineKeyboardButton('Зарегистрироватся', callback_data='reg')
btn_continue = InlineKeyboardButton('Главное меню', callback_data='continue1')
btn_yes = InlineKeyboardButton('Да', callback_data='yes')
btn_no = InlineKeyboardButton('Нет', callback_data='no')
btn_yes2 = InlineKeyboardButton('Да', callback_data='yes2')
btn_no2 = InlineKeyboardButton('Нет', callback_data='no2')
btn_to_subject_list = InlineKeyboardButton('Предметы', callback_data="subject_list")

# * Клавиатурки
# TODO: Переделать главное меню

kb_yes_or_no = InlineKeyboardMarkup().add(btn_yes).add(btn_no)
kb_yes_or_no2 = InlineKeyboardMarkup().add(btn_yes2).add(btn_no2)
kb_start = InlineKeyboardMarkup().add(btn_reg).add(btn_continue)
kb_continue_to_main_menu = InlineKeyboardMarkup().add(btn_continue).add(btn_to_subject_list)
kb_reg = InlineKeyboardMarkup().add(btn_reg)
kb_subject_list = InlineKeyboardMarkup().add(btn_to_subject_list)
kb_retry = InlineKeyboardMarkup().add(btn_continue).add(btn_to_subject_list)

# ? Старт

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Этот бот был создан для наглядной демонстрации изменения оценок, по тому или иному предмету. \n", reply_markup=kb_start)

@dp.callback_query_handler(text=['continue1'])
async def call_main_menu(call: types.CallbackQuery):
    await call.message.delete()
    user_id = call.from_user.id
    id_list = select_id()
    if str(user_id) in id_list:
        await call.message.answer('Добрый день. Если хотите выстроить график нажмите кнопку "Предметы" ниже.', reply_markup=kb_continue_to_main_menu)
    else:
        await call.message.answer('Извините, но вы не зарегестрированы. Нажмите на кнопку "Зарегистрироватся" ниже', reply_markup=kb_reg)

# ? Лист предметов
# TODO: Расширить, добавит изображение

@dp.callback_query_handler(text=['subject_list'])
async def call_SubjectList(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("""
Индивидуальный проект
                              Иностранный язык 
                              Литература
                              Русский язык
                              Алгебра
                              Геометрия
                              Информатика
                              Технология
                              Биология
                              География
                              Физика
                              Химия
                              История
                              Обществознание
                              ОБЖ
                              Физическая культура""")
    await call.message.answer("Напишите в ответ предмет, по которому хотели построить график, пожалуйста соблюдайте регистр и раскладку.")
    await SubjectState.Subject.set()

@dp.message_handler(state=SubjectState.Subject)
async def select_subject(message: types.Message, state: FSMContext):
    await state.update_data(subject=message.text)
    await message.answer("Отлично! Теперь напишите четверть.")

    await SubjectState.next()

@dp.message_handler(state=SubjectState.Quarter)
async def select_quarter(message: types.Message, state: FSMContext):
    await state.update_data(quarter=message.text)
    data = await state.get_data()
    await message.answer(f"Предмет: {data['subject']}\n"
                         f"Четверть {data['quarter']}\n"
                         "Всё верно?", reply_markup=kb_yes_or_no2)

    await state.reset_state(with_data=False)

@dp.callback_query_handler(text='yes2')
async def yes2(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.delete()
        data = await state.get_data()
        await call.message.answer("Постройка графика занимает от 2 до 3 минут, пожалуйста подождите.")

        filename = f'{data["subject"]}_{data["quarter"]}{call.from_user.id}'

        data = await state.get_data()

        print(data)

        subject = CreateFile(select_user_data(call.from_user.id), int(data['quarter']), data["subject"], filename)
        subject.create_image()

        path = Path(filename)

        photo = InputFile(f'{path}.png')
        await bot.send_photo(call.from_user.id, photo=photo)
    
    except Exception:
        await call.message.answer("Извините, что то пошло не так. Сбой может быть связан со следующими причинами: \n 1.Сбой сетевого города \n 2.Не стабильное или медленное подключение к интернету \n 3. Невозможно вывести график по данному предмету")
        await call.message.answer("Попробуйте ещё раз позже", reply_markup=kb_retry)



    await state.finish()

@dp.callback_query_handler(text='no2')
async def no2(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Нажмите на кнопку ниже, чтобы изменить предмет.", reply_markup=kb_subject_list)

    await state.finish()


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


@dp.callback_query_handler(text='chemist')
async def call_chemist(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Введите цифрой четверть которую хотите увидеть: ")
    quarter = 2
    await call.message.answer(quarter)
    print(quarter, type(quarter))

if __name__ == '__main__':
    executor.start_polling(dp)