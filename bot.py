import asyncio
import os
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("TOKEN")
API_KEY = os.getenv("API_KEY")

if not TOKEN:
    print("🚫 TOKEN не найден!")
    exit()

headers = {
    "X-RapidAPI-Key": API_KEY or "",
    "X-RapidAPI-Host": "v3.football.api-sports.io"
}

async def get_matches(league_id, league_name):
    """Реальные матчи"""
    try:
        url = "https://v3.football.api-sports.io/fixtures"
        params = {"date": "2026-03-09", "league": str(league_id), "season": "2025"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    matches = data["response"][:3]
                    if matches:
                        result = f"⚽ <b>{league_name}:</b>\n\n"
                        for match in matches:
                            home = match["teams"]["home"]["name"]
                            away = match["teams"]["away"]["name"]
                            time = match["fixture"]["date"][11:16]
                            result += f"• <b>{home}</b> vs <b>{away}</b> ({time})\n"
                        return result
    except:
        pass
    return f"⚽ Матчей {league_name} сегодня нет"

bot = Bot(token=TOKEN)
dp = Dispatcher()  # ← ЭТО ЗДЕСЬ!

@dp.message(Command("start"))
async def start(message:


