import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("TOKEN")
API_KEY = os.getenv("API_KEY")

if not TOKEN:
    print("🚫 TOKEN не найден!")
    exit()

# 5 ЛИГ — ВСЕ МАТЧИ ТУРА (14-15 марта 2026)
LEAGUES = {
    "rpl": {
        "flag": "🇷🇺", "name": "РПЛ", "matches": [
            ("Спартак", "Краснодар", "14.03 18:00"),
            ("Зенит", "Динамо М", "14.03 20:30"), 
            ("ЦСКА", "Локомотив", "15.03 15:00"),
            ("Крылья Советов", "Рубин", "15.03 17:30"),
            ("Факел", "Урал", "15.03 20:00"),
            ("Динамо СПб", "Акрон", "14.03 19:00")
        ]
    },
    "epl": {
        "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "name": "АПЛ", "matches": [
            ("Арсенал", "Ман Сити", "14.03 17:30"),
            ("Ливерпуль", "Челси", "14.03 20:00"),
            ("МЮ", "Тоттенхэм", "15.03 16:00"),
            ("Ньюкасл", "Вест Хэм", "14.03 15:00"),
            ("Брайтон", "Вулверхэмптон", "14.03 20:00"),
            ("Эвертон", "Борнмут", "15.03 14:00")
        ]
    },
    "laliga": {
        "flag": "🇪🇸", "name": "Ла Лига", "matches": [
            ("Реал Мадрид", "Барселона", "14.03 21:00"),
            ("Атлетико М", "Севилья", "15.03 19:00"),
            ("Валенсия", "Атлетик Б", "15.03 17:00"),
            ("Бетис", "Вильярреал", "14.03 20:00"),
            ("Жирона", "Осасуна", "15.03 15:00"),
            ("Алавес", "Мальорка", "14.03 19:00")
        ]
    },
    "ligue1": {
        "flag": "🇫🇷", "name": "Лига 1", "matches": [
            ("ПСЖ", "Монако", "14.03 19:45"),
            ("Лион", "Марсель", "15.03 18:00"),
            ("Лилль", "Ницца", "15.03 20:00"),
            ("Ренн", "Монпелье", "14.03 20:00"),
            ("Тулуза", "Брест", "15.03 16:00"),
            ("Ланс", "Реймс", "14.03 19:00")
        ]
    },
    "bundesliga": {
        "flag": "🇩🇪", "name": "Бундеслига", "matches": [
            ("Бавария", "Боруссия Д", "14.03 18:30"),
            ("Боруссия М", "РБ Лейпциг", "14.03 20:30"),
            ("Байер Л", "Штутгарт", "15.03 16:30"),
            ("Айнтрахт", "Вердер", "14.03 19:30"),
            ("Унион Б", "Фрайбург", "15.03 15:30"),
            ("Кёльн", "Гамбург", "14.03 20:00")
        ]
    }
}

def get_match_forecast(home, away, date):
    """Прогноз для матча"""
    probs = {
        "П1": 55, "X": 25, "П2": 20,
        "ТБ2.5": 60, "ТМ2.5": 40,
        "ТБ9.5угл": 58, "ТБ4.5карт": 65
    }
    
    result = f"🔮 <b>{home} vs {away}</b>\n"
    result += f"📅 <b>{date}</b>\n\n"
    
    result += f"📊 <b>ТОП-3 СТАВКИ:</b>\n"
    bets = [
        (f"П1 {probs['П1']}%", f"КФ {1.6+probs['П1']/100:.2f}"),
        (f"ТБ2.5 {probs['ТБ2.5']}%", f"КФ {1.75+probs['ТБ2.5']/100:.2f}"),
        (f"ТБ4.5 карт. {probs['ТБ4.5карт']}%", f"КФ {1.85+probs['ТБ4.5карт']/100:.2f}")
    ]
    
    for bet_name, kf in bets:
        result += f"• <b>{bet_name} ({kf})</b>\n"
    
    return result

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📅 Все матчи тура", callback_data="all_tour")],
        [InlineKeyboardButton(text="🔮 Топ-прогнозы", callback_data="top_forecasts")],
        [InlineKeyboardButton(text="📊 Выбрать лигу", callback_data="leagues")]
    ])
    await message.answer(
        "⚽ <b>СТАВКИ v6.1 — ВСЕ МАТЧИ ТУРА</b>\n\n"
        "✅ <b>30+ матчей</b> 5 лиг\n"
        "✅ <b>Каждый матч</b> с датой и прогнозами\n"
        "✅ <b>Топ-3 ставки</b> для каждого матча\n\n"
        "Выбери:", 
        reply_markup=keyboard, 
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "all_tour")
async def all_tour_matches(callback: types.CallbackQuery):
    result = "📅 <b>ТУР 5 ЛИГ (14-15 марта)</b>\n\n"
    
    total_matches = 0
    for code, league in LEAGUES.items():
        result += f"{league['flag']} <b>{league['name']} ({len(league['matches'])} матчей)</b>\n"
        for home, away, date in league['matches'][:2]:
            result += f"  • {home[:15]} vs {away[:15]} ({date})\n"
        result += "\n"
        total_matches += len(league['matches'])
    
    result += f"<b>ВСЕГО: {total_matches} матчей!</b>"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 РПЛ (6)", callback_data="rpl_tour")],
        [InlineKeyboardButton(text="🏴󠁧󠁢󠁥󠁮󠁧󠁿 АПЛ (6)", callback_data="epl_tour")],
        [InlineKeyboardButton(text="🇪🇸 Ла Лига (6)", callback_data="laliga_tour")],
        [InlineKeyboardButton(text="🇫🇷 Лига 1 (6)", callback_data="ligue1_tour")],
        [InlineKeyboardButton(text="🇩🇪 Бундеслига (6)", callback_data="bundesliga_tour")]
    ])
    
    await callback.message.edit_text(result, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data.endswith("_tour"))
async def league_tour(callback: types.CallbackQuery):
    league_code = callback.data.split("_")[0]
    league = LEAGUES[league_code]
    
    result = f"{league['flag']} <b>{league['name']} — ВСЕ МАТЧИ ТУРА</b>\n\n"
    
    match_keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for i, (home, away, date) in enumerate(league['matches']):
        btn_text = f"{home[:12]} vs {away[:12]}"
        match_keyboard.inline_keyboard.append([
            InlineKeyboardButton(text=btn_text, callback_data=f"match_{league_code}_{i}")
        ])
        
        result += f"{i+1}. <b>{home}</b> vs <b>{away}</b>\n"
        result += f"   📅 {date}\n\n"
    
    back_btn = InlineKeyboardButton(text="⬅️ Назад", callback_data="all_tour")
    match_keyboard.inline_keyboard.append([back_btn])
    
    await callback.message.edit_text(result, reply_markup=match_keyboard, parse_mode="HTML")
    await callback.answer(f"{len(league['matches'])} матчей {league['name']}")

@dp.callback_query(F.data.startswith("match_"))
async def match_detail(callback: types.CallbackQuery):
    _, league_code, match_idx = callback.data.split("_")
    match_idx = int(match_idx)
    league = LEAGUES[league_code]
    
    home, away, date = league['matches'][match_idx]
    forecast = get_match_forecast(home, away, date)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Все матчи лиги", callback_data=f"{league_code}_tour")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="start")]
    ])
    
    await callback.message.edit_text(forecast, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer(f"Прогноз: {home} vs {away}")

@dp.callback_query(F.data == "top_forecasts")
async def top_forecasts(callback: types.CallbackQuery):
    result = "🏆 <b>ТОП-6 ПРОГНОЗОВ ТУРА</b>\n\n"
    
    top_matches = [
        ("Реал Мадрид vs Барселона", "ТБ2.5 60%"),
        ("Бавария vs Боруссия Д", "П1 65%"),
        ("Арсенал vs Ман Сити", "ТБ9.5 угл. 58%"),
        ("Спартак vs Краснодар", "ТБ4.5 карт. 65%"),
        ("ПСЖ vs Монако", "П1 62%"),
        ("Зенит vs Динамо", "ТБ2.5 60%")
    ]
    
    for match, bet in top_matches:
        result += f"• <b>{match}</b>\n  {bet}\n\n"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📅 Все матчи", callback_data="all_tour")]
    ])
    
    await callback.message.answer(result, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "leagues")
async def league_menu(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📅 Все матчи тура", callback_data="all_tour")],
        [InlineKeyboardButton(text="🔮 Топ-прогнозы", callback_data="top_forecasts")]
    ])
    await callback.message.edit_text("🏠 <b>ГЛАВНОЕ МЕНЮ</b>", reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()

@dp.message(Command("predict"))
async def cmd_predict(message: types.Message):
    forecast = get_match_forecast("Спартак", "Краснодар", "14.03 18:00")
    await message.answer(forecast, parse_mode="HTML")

@dp.message()
async def echo(message: types.Message):
    await message.answer("📱 /start — 30+ матчей 5 лиг с прогнозами!\n⚽ Каждый матч → Топ-3 ставки")

async def main():
    print("🚀 СТАВКИ v6.1 — ВСЕ МАТЧИ 5 ЛИГ!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
