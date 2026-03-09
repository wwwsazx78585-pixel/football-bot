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
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "v3.football.api-sports.io"
}

async def get_matches(league_id, league_name):
    """Реальные матчи любой лиги"""
    url = "https://v3.football.api-sports.io/fixtures"
    params = {
        "date": "2026-03-09",
        "league": str(league_id),
        "season": "2025"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    matches = data["response"][:3]
                    if matches:
                        result = f"⚽ <b>{league_name} ({league_id}):</b>\n\n"
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
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚽ Сегодня", callback_data="today")],
        [InlineKeyboardButton(text="🔮 Прогноз", callback_data="predict")],
        [InlineKeyboardButton(text="📊 Лиги", callback_data="leagues")]
    ])
    await message.answer(
        "⚽ <b>ФУТБОЛЬНЫЙ БОТ v2.0</b>\n\n"
        "✅ Реальные матчи из 5 лиг!\n"
        "✅ API-Football\n"
        "✅ 24/7 онлайн", 
        reply_markup=keyboard, 
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "today")
async def today(callback: types.CallbackQuery):
    matches = await get_matches("39", "🇷🇺 РПЛ")
    await callback.message.answer(matches, parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "predict")
async def predict(callback: types.CallbackQuery):
    await callback.message.answer(
        "🔮 <b>ПРОГНОЗ ДНЯ:</b>\n\n"
        "🏠 <b>Спартак</b> 2:1 <b>Зенит</b>\n"
        "⏰ 18:00 РПЛ\n\n"
        "💰 <b>П1 @2.10</b>\n"
        "📊 65% | 20% | 15%", 
        parse_mode="HTML"
    )
    await callback.answer()

@dp.callback_query(F.data == "leagues")
async def leagues_menu(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 РПЛ", callback_data="rpl")],
        [InlineKeyboardButton(text="🏴󠁧󠁢󠁥󠁮󠁧󠁿 АПЛ", callback_data="epl")],
        [InlineKeyboardButton(text="🇪🇸 Ла Лига", callback_data="laliga")],
        [InlineKeyboardButton(text="⭐ ЛЧ", callback_data="ucl")]
    ])
    await callback.message.edit_text(
        "📊 <b>ВЫБЕРИ ЛИГУ:</b>", 
        reply_markup=keyboard, 
        parse_mode="HTML"
    )
    await callback.answer()

@dp.callback_query(F.data == "rpl")
async def rpl(callback: types.CallbackQuery):
    matches = await get_matches("39", "🇷🇺 РПЛ")
    await callback.message.answer(matches, parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "epl")
async def epl(callback: types.CallbackQuery):
    matches = await get_matches("40", "🏴󠁧󠁢󠁥󠁮󠁧󠁿 АПЛ")
    await callback.message.answer(matches, parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "laliga")
async def laliga(callback: types.CallbackQuery):
    matches = await get_matches("140", "🇪🇸 Ла Лига")
    await callback.message.answer(matches, parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "ucl")
async def ucl(callback: types.CallbackQuery):
    matches = await get_matches("2", "⭐ ЛЧ")
    await callback.message.answer(matches, parse_mode="HTML")
    await callback.answer()

@dp.message()
async def echo(message: types.Message):
    await message.answer("📱 /start — главное меню")

async def main():
    print("🚀 Бот с 5 лигами запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

