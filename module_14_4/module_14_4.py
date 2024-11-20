from gettext import textdomain
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import  FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import  InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import initiate_db, get_all_products
from aiohttp.helpers import PY_310

api = "code"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb1 = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text="Рассчитать")
button2 = KeyboardButton(text="Информация")
button3 = KeyboardButton(text='Купить')
kb1.add(button1, button2, button3)


kb2 = InlineKeyboardMarkup(resize_keyboard=True)
b1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
b2 = InlineKeyboardButton(text='Формула расчёта', callback_data='formula')
P1 = InlineKeyboardButton(text="Product1", callback_data="product_buying")
P2 = InlineKeyboardButton(text="Product2", callback_data="product_buying")
P3 = InlineKeyboardButton(text="Product3", callback_data="product_buying")
P4 = InlineKeyboardButton(text="Product4", callback_data="product_buying")
kb2.add(b1, b2)

product_menu = InlineKeyboardMarkup(resize_keyboard=True)
product_menu.add(P1, P2, P3, P4)


@dp.message_handler(commands=["start"])
async def start_message(message):
    await message.answer("Привет, я бот, который поможет твоему здоровью. Введи: Рассчитать норму калорий", reply_markup = kb1)

@dp.message_handler(text="Информация")
async def info_message(message):
    await message.answer("Инфа про бота!")

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию.', reply_markup=kb2)

@dp.callback_query_handler(text='formula')
async def get_formula(call):
    await call.message.answer('(10 х вес в кг) + (6,25 х рост в см) – (5 х возраст в г) – 161')
    await call.answer()


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    products = get_all_products()

    for product in products:
        with open('medicine.jpg', 'rb') as img:
            product_name = product[1]
            product_description = product[2]
            product_price = product[3]

            await message.answer_photo(
                img,
                f'Название: {product_name} | Описание: {product_description} | Цена: {product_price}'
            )

    await message.answer("Выберите продукт для покупки:", reply_markup=product_menu)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.callback_query_handler(text= "calories")
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    data = await state.get_data()
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    data = await state.get_data()
    await message.answer('Введите свой вес в кг:')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    calories = 10 * weight + 6.25 * growth - 5 * age - 161
    await message.answer(calories)
    await state.finish()

@dp.message_handler()
async def all_messages(message):
    print("Новое сообщение!")
    await message.answer('Пиши команду /start')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
