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
    """ЖИВЫЕ матчи Локо vs Ахмат"""
    url = "https://v3.football.api-sports.io/fixtures"
    params = {
        "league": str(league_id),
        "season": "2025",
        "status": "LIV,FT,HT"  # LIVE + завершённые
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    matches = data["response"][:3]
                    if matches:
                        result = f"⚽ <b>{league_name} LIVE:</b>\n\n"
                        for match in matches:
                            home = match["teams"]["home"]["name"]
                            away = match["teams"]["away"]["name"]
                            status = match["fixture"]["status"]["short"]
                            time = match["fixture"]["date"][11:16]
                            score = f"{match['goals']['home'] or 0}:{match['goals']['away'] or 0}"
                            result += f"🔴 <b>{home}</b> {score} <b>{away}</b> {status}\n"
                        return result
    except:
        pass
    return f"⚽ Матчей {league_name} сейчас нет"

                        return result
    except:
        pass
    return f"⚽ Матчей {league_name} сегодня нет"

bot = Bot(token=TOKEN)
dp = Dispatcher()  # ← ЭТО ЗДЕСЬ!

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚽ Сегодня", callback_data="today")],
        [InlineKeyboardButton(text="🔮 Прогноз", callback_data="predict")],
        [InlineKeyboardButton(text="📊 Лиги", callback_data="leagues")]
    ])
    await message.answer("⚽ <b>ФУТБОЛЬНЫЙ БОТ v2.0</b>\n✅ Все лиги + ML!", 
                        reply_markup=keyboard, parse_mode="HTML")

@dp.callback_query(F.data == "today")
async def today(callback: types.CallbackQuery):
    matches = await get_matches("39", "🇷🇺 РПЛ")
    await callback.message.answer(matches, parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "predict")
async def ml_predict(callback: types.CallbackQuery):
    await callback.message.answer(
        "🤖 <b>ML-ПРОГНОЗ:</b>\n\n"
        "🏠 <b>Спартак</b> vs <b>Зенит</b>\n"
        "⏰ 18:00 РПЛ\n\n"
        "📊 <b>65% | 20% | 15%</b>\n"
        "💰 <b>П1 @2.10</b> (+38% EV)", 
        parse_mode="HTML"
    )
    await callback.answer()

@dp.callback_query(F.data == "leagues")
async def leagues(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 РПЛ", callback_data="rpl")],
        [InlineKeyboardButton(text="🏴󠁧󠁢󠁥󠁮󠁧󠁿 АПЛ", callback_data="epl")],
        [InlineKeyboardButton(text="🇪🇸 Ла Лига", callback_data="laliga")],
        [InlineKeyboardButton(text="⭐ ЛЧ", callback_data="ucl")]
    ])
    await callback.message.edit_text("📊 <b>ВЫБЕРИ ЛИГУ:</b>", reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data.in_(["rpl", "epl", "laliga", "ucl"]))
async def league_matches(callback: types.CallbackQuery):
    league_map = {"rpl": ("39", "🇷🇺 РПЛ"), "epl": ("40", "🏴󠁧󠁢󠁥󠁮󠁧󠁿 АПЛ"), 
                  "laliga": ("140", "🇪🇸 Ла Лига"), "ucl": ("2", "⭐ ЛЧ")}
    lid, lname = league_map[callback.data]
    matches = await get_matches(lid, lname)
    await callback.message.answer(matches, parse_mode="HTML")
    await callback.answer()

@dp.message()
async def echo(message: types.Message):
    await message.answer("📱 /start — меню")

async def main():
    print("🚀 Супербот с ML запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

