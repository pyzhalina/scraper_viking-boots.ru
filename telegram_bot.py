import json

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold

import auth_data
from main import collect_data

bot = Bot(token=auth_data.TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Обувь (распродажа)']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Товары со скидкой", reply_markup=keyboard)

@dp.message_handler(Text(equals='Обувь (распродажа)'))
async def get_discount_boots(message: types.Message):
    await message.answer("Пожалуйста, подождите...")

    collect_data(file_path=r'C:\Users\covsh\PycharmProjects\scraper viking-boots.ru\page.html')

    with open("result.json") as file:
        data = json.load(file)

    for item in data:
        card = f"{item.get('link')}\n" \
               f"{hbold('Цена: ')} {item.get('new price')}\n" \
               f"{hbold('Скидка: ')} {item.get('discount percent')}🔥\n" \
               f"{hbold('Цена без скидки: ')} {item.get('old price')}"


        await message.answer(card)

def main():
    executor.start_polling(dp)

if __name__ == '__main__':
    main()