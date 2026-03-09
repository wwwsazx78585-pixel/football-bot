import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Читаем токен из переменных Railway (или жёстко для теста)
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("🚫 TOKEN не найден! Добавь переменную TOKEN на Railway")

print(f"🚀 TOKEN получен, длина: {len(TOKEN)} символов")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("⚽ ФУТБОЛЬНЫЙ БОТ РАБОТАЕТ!\n\n/predict — получить прогноз")

@dp.message(Command("predict"))
async def predict(message: types.Message):
    await message.answer("🔮 <b>Прогноз дня:</b>\nСпартак 2:1 Зенит\n\n💰 Ставка: П1", parse_mode="HTML")

@dp.message()
async def echo(message: types.Message):
    await message.answer("📱 Пиши /start или /predict")

async def main():
    print("🚀 Запускаем бот...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

