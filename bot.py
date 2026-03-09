import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("🚫 TOKEN не найден!")
    exit()

# ⚡ СУПЕР-БЫСТРЫЕ ДАННЫЕ (без API)
LEAGUES = {
    "ucl": {
        "flag": "⭐", "name": "ЛЧ 1/8", "matches": [
            ("ПСЖ", "Челси", "10.03 21:00"),
            ("Реал", "Сити", "11.03 21:00"),
            ("Аталанта", "Бавария", "11.03 21:00")
        ]
    },
    "rpl": {
        "flag": "🇷🇺", "name": "РПЛ", "matches": [
            ("Спартак", "Краснодар", "14.03 18:00"),
            ("Зенит", "Динамо", "14.03 20:30"),
            ("ЦСКА", "Локо", "15.03 15:00")
        ]
    }
}

def get_forecast(home, away, date):
    return f"""🔮 <b>{home} vs {away}</b>
📅 <b>{date}</b>

📊 <b>СТАВКИ:</b>
• П1 <b>58% (КФ 1.72)</b>
• ТБ2.5 <b>62% (КФ 1.85)</b>
• ТБ9.5 угл. <b>59% (КФ 1.78)</b>"""

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⭐ ЛЧ", callback_data="ucl")],
        [InlineKeyboardButton(text="🇷🇺 РПЛ", callback_data="rpl")],
        [InlineKeyboardButton(text="🔮 Топ", callback_data="top")]
    ])
    await message.answer(
        "⚽ <b>СТАВКИ v6.6 — МОЛНИЕНОСНЫЙ</b>\n\n"
        "⭐ ЛЧ 1/8 | 🇷🇺 РПЛ\n"
        "✅ <b>0.5 сек ответ</b>\n✅ Топ-3 ставки", 
        reply_markup=keyboard, parse_mode="HTML"
    )

@dp.callback_query(F.data.in_(["ucl", "rpl"]))
async def league_menu(callback: types.CallbackQuery):
    league = LEAGUES[callback.data]
    result = f"{league['flag']} <b>{league['name']}</b>\n\n"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for i, (home, away, date) in enumerate(league['matches']):
        btn_text = f"{home[:8]} vs {away[:8]}"
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text=btn_text, callback_data=f"m_{callback.data}_{i}")
        ])
        result += f"{i+1}. <b>{home}</b> vs <b>{away}</b>\n"
    
    keyboard.inline_keyboard.append([InlineKeyboardButton(text="🏠", callback_data="start")])
    await callback.message.edit_text(result, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data.startswith("m_"))
async def match_forecast(callback: types.CallbackQuery):
    _, league, idx = callback.data.split("_")
    league_data = LEAGUES[league]
    home, away, date = league_data["matches"][int(idx)]
    
    forecast = get_forecast(home, away, date)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️", callback_data=league)],
        [InlineKeyboardButton(text="🏠", callback_data="start")]
    ])
    
    await callback.message.edit_text(forecast, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "top")
async def top_bets(callback: types.CallbackQuery):
    result = "🔥 <b>ТОП-3 СТАВКИ:</b>\n\n• ПСЖ vs Челси: <b>ТБ2.5 62%</b>\n• Реал vs Сити: <b>П1 58%</b>\n• Спартак vs Краснодар: <b>ТБ4.5 карт. 65%</b>"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⭐ ЛЧ", callback_data="ucl")],
        [InlineKeyboardButton(text="🇷🇺 РПЛ", callback_data="rpl")]
    ])
    await callback.message.answer(result, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "start")
async def main_menu(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⭐ ЛЧ", callback_data="ucl")],
        [InlineKeyboardButton(text="🇷🇺 РПЛ", callback_data="rpl")],
        [InlineKeyboardButton(text="🔮 Топ", callback_data="top")]
    ])
    await callback.message.edit_text(
        "⚽ <b>СТАВКИ v6.6 — СУПЕР БЫСТРО!</b>\n⭐ ЛЧ | 🇷🇺 РПЛ\n✅ 0.5 сек ответ", 
        reply_markup=keyboard, parse_mode="HTML"
    )
    await callback.answer()

@dp.message()
async def echo(message: types.Message):
    await message.answer("🚀 /start — молниеносные ставки!")

async def main():
    print("🚀 v6.6 МОЛНИЕНОСНЫЙ БОТ!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
