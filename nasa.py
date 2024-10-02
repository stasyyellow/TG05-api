import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
import requests
from datetime import datetime
from config import TOKEN, NASA_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для получения изображения по введенной дате
def get_apod_by_date(date_str: str):
    url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={date_str}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Команда /start для приветствия
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Я бот, который покажет снимок NASA. Напиши дату в формате 'год-месяц-день', чтобы получить фото.")

# Функция для обработки сообщений с датой
@dp.message(F.text)
async def apod_by_date(message: Message):
    date_str = message.text.strip()

    try:
        # Проверяем корректность формата даты
        datetime.strptime(date_str, "%Y-%m-%d")
        apod = get_apod_by_date(date_str)

        if apod and 'url' in apod:
            photo_url = apod['url']
            title = apod['title']
            await message.answer_photo(photo=photo_url, caption=f"{title}")
        else:
            await message.answer("Не удалось найти фотографию на указанную дату.")
    except ValueError:
        await message.answer("Пожалуйста, введи дату в формате 'год-месяц-день'.")

# Основная функция запуска бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
