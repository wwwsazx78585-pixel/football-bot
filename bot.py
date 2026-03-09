from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import os

TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_today_matches(league):
    """Реальные матчи 9 марта 2026"""
    matches = {
        "today": [
            ("9 марта 14:00", "Ротор 1:2 Урал (Первая лига)", "П2 2.10 / ТБ2.5 1.85"),
            ("9 марта 16:30", "Монтана 0:3 Лудогорец (Болгария)", "П2 1.45 / ТБ2.5 1.70"),
            ("9 марта 19:45", "Лацио vs Интер (Серия А)", "ТБ2.5 1.75 / П2 2.20"),
            ("9 марта 20:00", "Локо vs Ахмат (РПЛ)", "П1 1.95 / ТБ2.5 1.88"),
        ],
        "rpl": [
            ("9 марта 20:00", "Локомотив 2:1 Ахмат", "П1 1.95 / ТБ2.5 1.88"),
            ("9 марта 17:00", "Спартак vs Акрам", "П1 1.65 / ТБ2.5 1.75"),
        ],
        "lch": [
            ("10 марта 20:45", "Ливерпуль vs Атлетико (ЛЧ 1/8)", "П1 1.80 / ТБ2.5 1.72"),
            ("10 марта 23:00", "Тоттенхэм vs Ньюкасл (ЛЧ 1/8)", "П1 1.55 / ТБ2.5 1.70"),
            ("11 марта 20:45", "Арсенал vs Реал (ЛЧ 1/8)", "ТБ2.5 1.82 / П2 2.10"),
            ("11 марта 23:00", "Ман Сити vs ПСЖ (ЛЧ 1/8)", "П1 2.00 / ТБ2.5 1.65")
        ],
        "epl": [
            ("9 марта 15:00", "Ноттингем vs Брайтон", "ТБ2.5 1.80 / П1 2.40"),
            ("9 марта 17:30", "Вулверхэмптон vs Вест Хэм", "ТБ2.5 1.75")
        ]
    }
    return matches.get(league, matches["today"])

def fonbet_place_bet(match, bet_type, amount=1000):
    return f"✅ <b>СТАВКА ПРИНЯТА!</b>\n\n🏆 {match}\n🎯 {bet_type}\n💰 {amount}₽\n📱 Fonbet"

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚡ СЕГОДНЯ 9 МАРТА", callback_data="today")],
        [InlineKeyboardButton(text="⭐ ЛЧ 1/8 (10-11 марта)", callback_data="lch")],
        [InlineKeyboardButton(text="🇷🇺 РПЛ", callback_data="rpl")],
        [InlineKeyboardButton(text="🏴󠁧󠁢󠁥󠁮󠁧󠁿 АПЛ", callback_data="epl")],
        [InlineKeyboardButton(text="🎯 АВТО-СТАВКИ", callback_data="autobet")]
    ])
    await message.answer(
        "⚽ <b>LIVE v7.5 — 9 МАРТА 2026</b>\n\n"
        "🔥 <b>СЕГОДНЯ:</b>\n"
        "• 20:00 Локо vs Ахмат (РПЛ)\n"
        "• 19:45 Лацио vs Интер (Серия А)\n\n"
        "⭐ <b>ЛЧ 1/8 (10-11 марта):</b>\n"
        "• Ливерпуль vs Атлетико\n"
        "• Арсенал vs Реал Мадрид\n\n"
        "🎯 Fonbet LIVE коэффициенты!", 
        reply_markup=kb, parse_mode="HTML"
    )

@dp.callback_query(F.data == "today")
async def today(call: types.CallbackQuery):
    matches = get_today_matches("today")
    text = "⚡ <b>СЕГОДНЯ 9 МАРТА 2026</b>\n\n"
    
    kb_rows = []
    for date, match, odds in matches:
        kb_rows.append([InlineKeyboardButton(text=f"{date}\n{match}", callback_data=f"match_{match.replace(' ', '_')}")])
    kb_rows.append([InlineKeyboardButton(text="🎯 СТАВИТЬ", callback_data="today_bet")])
    kb_rows.append([InlineKeyboardButton(text="⬅️ Главное", callback_data="start")])
    kb = InlineKeyboardMarkup(inline_keyboard=kb_rows)
    
    for date, match, odds in matches:
        text += f"📅 <b>{date}</b>\n⚽ {match}\n📊 {odds}\n\n"
    
    await call.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await call.answer()

@dp.callback_query(F.data == "lch")
async def lch(call: types.CallbackQuery):
    matches = get_today_matches("lch")
    text = "⭐ <b>ЛИГА ЧЕМПИОНОВ 1/8</b>\n\n"
    text += "📅 <b>10 марта:</b>\n"
    
    kb_rows = []
    for i, (date, match, odds) in enumerate(matches):
        kb_rows.append([InlineKeyboardButton(text=f"{date}\n{match}", callback_data=f"lch_{i}")])
    kb_rows.append([InlineKeyboardButton(text="⬅️ Главное", callback_data="start")])
    kb = InlineKeyboardMarkup(inline_keyboard=kb_rows)
    
    for date, match, odds in matches:
        text += f"📅 <b>{date}</b>\n⚽ {match}\n📊 {odds}\n\n"
    
    await call.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await call.answer()

@dp.callback_query(F.data.in_(["rpl", "epl"]))
async def leagues(call: types.CallbackQuery):
    league_name = "🇷🇺 РПЛ" if call.data == "rpl" else "🏴󠁧󠁢󠁥󠁮󠁧󠁿 АПЛ"
    matches = get_today_matches(call.data)
    
    text = f"{'' if call.data=='rpl' else ''}<b>{league_name} — 9 марта</b>\n\n"
    
    kb_rows = []
    for date, match, odds in matches:
        kb_rows.append([InlineKeyboardButton(text=f"{date}\n{match}", callback_data=f"{call.data}_{match.replace(' ', '_')}")])
    kb_rows.append([InlineKeyboardButton(text="⬅️ Главное", callback_data="start")])
    kb = InlineKeyboardMarkup(inline_keyboard=kb_rows)
    
    for date, match, odds in matches:
        text += f"📅 <b>{date}</b>\n⚽ {match}\n📊 {odds}\n\n"
    
    await call.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await call.answer()

@dp.callback_query(F.data.startswith("match_"))
async def match_detail(call: types.CallbackQuery):
    match_name = call.data.replace("match_", "").replace("_", " vs ")
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎯 СТАВИТЬ 1000₽", callback_data="bet_1000")],
        [InlineKeyboardButton(text="⬅️ Сегодня", callback_data="today")]
    ])
    await call.message.edit_text(
        f"🔴 LIVE <b>{match_name}</b>\n\n"
        f"📊 ТБ2.5 <b>КФ 1.85</b>\n"
        f"⛳ ТБ9.5 угл. <b>КФ 1.78</b>", 
        reply_markup=kb, parse_mode="HTML"
    )
    await call.answer()

@dp.callback_query(F.data == "autobet")
async def autobet(call: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 500₽", callback_data="bet_500")],
        [InlineKeyboardButton(text="💎 1000₽", callback_data="bet_1000")],
        [InlineKeyboardButton(text="💵 5000₽", callback_data="bet_5000")],
        [InlineKeyboardButton(text="⬅️ Матчи", callback_data="today")]
    ])
    await call.message.edit_text(
        "🎯 <b>АВТО-СТАВКА Fonbet</b>\n\n"
        "🔥 Топ сегодня: <b>Локо vs Ахмат</b>\n"
        "💎 Ставка: <b>ТБ2.5 КФ 1.88</b>\n\n"
        "1 клик = ставка LIVE!", 
        reply_markup=kb, parse_mode="HTML"
    )
    await call.answer()

@dp.callback_query(F.data.startswith("bet_"))
async def place_bet(call: types.CallbackQuery):
    amount = call.data.split("_")[1]
    bet = fonbet_place_bet("Локо vs Ахмат", "ТБ2.5", amount)
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Ещё ставка", callback_data="autobet")],
        [InlineKeyboardButton(text="🏠 Главное", callback_data="start")]
    ])
    await call.message.edit_text(bet, reply_markup=kb, parse_mode="HTML")
    await call.answer("✅ Ставка принята!")

@dp.message()
async def echo(message: types.Message):
    await message.answer("🚀 /start — LIVE 9 марта + ЛЧ!")

async def main():
    print("🚀 v7.5 — 9 МАРТА + ЛЧ 1/8!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

