import asyncio
import os
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta

TOKEN = os.getenv("TOKEN")
API_KEY = os.getenv("API_KEY")

if not TOKEN or not API_KEY:
    raise ValueError("🚫 TOKEN или API_KEY не найдены!")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Заголовки для API-Football
headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "v3.football.api-sports.io"
}

async def get_today_matches():
    """Получаем матчи на сегодня"""
    url = "https://v3.football.api-sports.io/fixtures"
    today = datetime.now().strftime("%Y-%m-%d")
    
    params = {
        "date": today,
        "league": "39",  # РПЛ
        "season": "2025"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data["response"][:3]  # Топ-3 матча
    return []

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚽ Сегодняшние матчи", callback_data="today")],
        [InlineKeyboardButton(text="🔮 Прогнозы", callback_data="predict")],
        [InlineKeyboardButton(text="📊 Топ-лиги", callback_data="leagues")]
    ])
    await message.answer(
        "⚽ <b>ФУТБОЛЬНЫЙ БОТ</b>\n\n"
        "Выбери действие:", 
        reply_markup=keyboard, 
        parse_mode="HTML"
    )

@dp.message(Command("predict"))
async def predict(message: types.Message):
    matches = await get_today_matches()
    if matches:
        match = matches[0]
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]
        time = match["fixture"]["date"][11:16]
        
        await message.answer(
            f"🔮 <b>Прогноз дня ({time}):</b>\n"
            f"🏠 <b>{home}</b> vs <b>{away}</b>\n\n"
            f"💰 <b>Рекомендация: П1</b>\n"
            f"Коэффициент: <code>2.10</code>", 
            parse_mode="HTML"
        )
    else:
        await message.answer("⚽ Матчей сегодня нет")

@dp.message()
async def echo(message: types.Message):
    await message.answer("📱 Выбери команду или нажми /start")

async def main():
    print("🚀 Футбольный бот с API запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
