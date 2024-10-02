#выводятся все валюты
import requests
import xml.etree.ElementTree as ET
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from config import TOKEN

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# URL API ЦБР для получения курсов валют
CBR_API_URL = 'https://www.cbr.ru/scripts/XML_daily.asp'

# Функция для получения курсов валют с сайта ЦБР
def get_exchange_rates():
    response = requests.get(CBR_API_URL)
    if response.status_code == 200:
        xml_data = ET.fromstring(response.content)
        rates = []
        for valute in xml_data.findall('Valute'):
            name = valute.find('Name').text
            char_code = valute.find('CharCode').text
            value = valute.find('Value').text
            nominal = valute.find('Nominal').text
            rates.append(f"{name} ({char_code}): {nominal} ед. = {value} RUB")
        return "\n".join(rates)
    return "Не удалось получить курсы валют."

# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет! Я бот для получения текущих курсов валют от Центробанка России. "
                         "Используй команду /exchange, чтобы узнать текущие курсы валют.")

# Обработчик команды /exchange
@dp.message(Command("exchange"))
async def send_exchange_rates(message: Message):
    rates = get_exchange_rates()
    await message.answer(rates)

# Основная функция запуска бота
async def main():
    # Регистрация обработчиков
    dp.message.register(send_welcome, Command("start"))
    dp.message.register(send_exchange_rates, Command("exchange"))

    # Запуск поллинга
    await dp.start_polling(bot)

# Запуск бота
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())