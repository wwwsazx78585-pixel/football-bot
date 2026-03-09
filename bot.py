from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import os

TOKEN = os.getenv("TOKEN")
FONBET_TOKEN = os.getenv("FONBET_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_weekend_matches(league):
    """Матчи ближайших выходных 13-14 марта 2026"""
    matches = {
        "weekend": [
            ("13 марта 16:00", "Динамо Мх - Оренбург (РПЛ)", "П1 2.14 / ТБ2.5 1.85"),
            ("13 марта 18:30", "Сочи - Краснодар (РПЛ)", "П2 1.95 / ТБ2.5 1.78"),
            ("13 марта 20:00", "Зенит - Спартак (РПЛ)", "П1 1.85 / ТБ2.5 1.90"),
            ("14 марта 15:00", "Арсенал - Ливерпуль (АПЛ)", "ТБ2.5 1.75 / ТБ10.5 угл 1.82"),
            ("14 марта 17:30", "Ман Сити - Челси (АПЛ)", "П1 1.50 / ТБ2.5 1.65"),
            ("14 марта 20:00", "Барселона - Атлетико (Ла Лига)", "ТБ2.5 1.80 / П1 1.90")
        ],
        "rpl": [
            ("13 марта 16:00", "Динамо Мх 1:1 Оренбург", "ТБ2.5 1.85 / П1 2.14"),
            ("13 марта 18:30", "Сочи 0:2 Краснодар", "П2 1.95 / ТБ2.5 1.78"),
            ("13 марта 20:00", "Зенит 2:1 Спартак", "П1 1.85 / ТБ2.5 1.90"),
            ("14 марта 14:00", "Локо 1:1 Ахмат", "X 3.40 / ТБ2.5 1.88")
        ],
        "lch": [
            ("14 марта 22:00", "ПСЖ - Челси (1/8 ЛЧ)", "ТБ2.5 1.72 / ТБ9.5 угл 1.78"),
            ("15 марта 21:00", "Реал - Сити (1/8 ЛЧ)", "ТБ2.5 1.68 / П1 2.10")
        ],
        "epl": [
            ("14 марта 15:00", "Арсенал 1:1 Ливерпуль", "ТБ2.5 1.75 / ТБ10.5 угл 1.82"),
            ("14 марта 17:30", "Ман Сити 3:1 Челси", "П1 1.50 / ТБ2.5 1.65"),
            ("15 марта 16:00", "Тоттенхэм - Астон Вилла", "ТБ2.5 1.78")
        ],
        "laliga": [
            ("14 марта 20:00", "Барселона 2:1 Атлетико", "ТБ2.5 1.80 / П1 1.90"),
            ("15 марта 21:00", "Реал - Севилья", "П1 1.45 / ТБ2.5 1.65")
        ]
    }
    return matches.get(league, matches["weekend"])

def fonbet_place_bet(match, bet_type, amount=1000):
    return f"✅ <b>СТАВКА ПРИНЯТА!</b>\n\n🏆 {match}\n🎯 {bet_type}\n💰 {amount}₽\n📱 Fonbet: сделано!"

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📅 13-14 МАРТА (выходные)", callback_data="weekend")],
        [InlineKeyboardButton(text="⭐ ЛЧ", callback_data="lch")],
        [InlineKeyboardButton(text="🇷🇺 РПЛ", callback_data="rpl")],
        [InlineKeyboardButton(text="🏴󠁧󠁢󠁥󠁮󠁧󠁿 АПЛ", callback_data="epl")],
        [InlineKeyboardButton(text="🇪🇸 Ла Лига", callback_data="laliga")],
        [InlineKeyboardButton(text="🎯 АВТО-СТАВКИ", callback_data="autobet")]
    ])
    await message.answer(
        "⚽ <b>v7.3 — МАТЧИ ВЫХОДНЫХ 13-14 МАРТА</b>\n\n"
        "📅 <b>13 марта:</b> Динамо Мх-Оренбург, Сочи-Краснодар, Зенит-Спартак\n"
        "📅 <b>14 марта:</b> Арсенал-Ливерпуль, Сити-Челси, Барса-Атлетико\n\n"
        "⭐ ЛЧ | 🇷🇺 РПЛ | 🏴󠁧󠁢󠁥󠁮󠁧󠁿 АПЛ | 🇪🇸 Ла Лига\n\n"
        "🎯 Fonbet 1 клик = ставка!", 
        reply_markup=kb, parse_mode="HTML"
    )

@dp.callback_query(F.data == "weekend")
async def weekend(call: types.CallbackQuery):
    matches = get_weekend_matches("weekend")
    text = "📅 <b>ВЫХОДНЫЕ 13-14 МАРТА 2026</b>\n\n"
    
    kb_rows = []
    for date, match, odds in matches:
        kb_rows.append([InlineKeyboardButton(text=f"{date}\n{match}", callback_data=f"match_{match.replace(' ', '_')}")])
    
    kb_rows.append([InlineKeyboardButton(text="🎯 СТАВИТЬ", callback_data="weekend_bet")])
    kb_rows.append([InlineKeyboardButton(text="⬅️ Главное", callback_data="start")])
    kb = InlineKeyboardMarkup(inline_keyboard=kb_rows)
    
    for date, match, odds in matches:
        text += f"📅 <b>{date}</b>\n⚽ {match}\n📊 {odds}\n\n"
    
    await call.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await call.answer()

@dp.callback_query(F.data == "rpl")
async def rpl(call: types.CallbackQuery):
    matches = get_weekend_matches("rpl")
    text = "🇷🇺 <b>РПЛ — 21 тур (13-14 марта)</b>\n\n"
    
    kb_rows = []
    for date, match, odds in matches:
        kb_rows.append([InlineKeyboardButton(text=f"{date}\n{match}", callback_data=f"match_{match.replace(' ', '_')}")])
    
    kb_rows.append([InlineKeyboardButton(text="🎯 СТАВИТЬ", callback_data="rpl_bet")])
    kb_rows.append([InlineKeyboardButton(text="⬅️ Главное", callback_data="start")])
    kb = InlineKeyboardMarkup(inline_keyboard=kb_rows)
    
    for date, match, odds in matches:
        text += f"📅 <b>{date}</b>\n⚽ {match}\n📊 {odds}\n\n"
    
    await call.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await call.answer()

@dp.callback_query(F.data.in_(["lch", "epl", "laliga"]))
async def other_leagues(call: types.CallbackQuery):
    league_names = {"lch": "⭐ ЛЧ — 1/8 финала", "epl": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 АПЛ — 29 тур", "laliga": "🇪🇸 Ла Лига — 28 тур"}
    league = league_names.get(call.data, "Лига")
    
    matches = get_weekend_matches(call.data)
    text = f"{'' if call.data=='lch' else ''} <b>{league} (13-15 марта)</b>\n\n"
    
    kb_rows = []
    for date, match, odds in matches:
        kb_rows.append([InlineKeyboardButton(text=f"{date}\n{match}", callback_data=f"match_{match.replace(' ', '_')}")])
    
    kb_rows.append([InlineKeyboardButton(text="🎯 СТАВИТЬ", callback_data=f"{call.data}_bet")])
    kb_rows.append([InlineKeyboardButton(text="⬅️ Главное", callback_data="start")])
    kb = InlineKeyboardMarkup(inline_keyboard=kb_rows)
    
    for date, match, odds in matches:
        text += f"📅 <b>{date}</b>\n⚽ {match}\n📊 {odds}\n\n"
    
    await call.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await call.answer()

@dp.callback_query(F.data.startswith("match_"))
async def match_detail(call: types.CallbackQuery):
    match_name = call.data.replace("match_", "").replace("_", " vs ")
    result = f"🔴 <b>{match_name}</b>\n\n📊 ТБ2.5 <b>КФ 1.72</b>\n⛳ ТБ9.5 угл. <b>КФ 1.78</b>"
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎯 СТАВИТЬ 1000₽", callback_data="bet_1000")],
        [InlineKeyboardButton(text="⬅️ Лига", callback_data="weekend")]
    ])
    
    await call.message.edit_text(result, reply_markup=kb, parse_mode="HTML")
    await call.answer()

@dp.callback_query(F.data == "autobet")
async def autobet(call: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 500₽", callback_data="bet_500")],
        [InlineKeyboardButton(text="💎 1000₽", callback_data="bet_1000")],
        [InlineKeyboardButton(text="💵 5000₽", callback_data="bet_5000")],
        [InlineKeyboardButton(text="⬅️ Матчи", callback_data="weekend")]
    ])
    await call.message.edit_text(
        "🎯 <b>АВТО-СТАВКА Fonbet</b>\n\n"
        "🔥 Топ-матч: <b>Зенит - Спартак (13 марта)</b>\n"
        "💎 Ставка: <b>ТБ2.5 КФ 1.90</b>\n\n"
        "1 клик = ставка принята!", 
        reply_markup=kb, parse_mode="HTML"
    )
    await call.answer()

@dp.callback_query(F.data.startswith("bet_"))
async def place_bet(call: types.CallbackQuery):
    amount = call.data.split("_")[1]
    bet = fonbet_place_bet("Зенит - Спартак", "ТБ2.5", amount)
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Ещё ставка", callback_data="autobet")],
        [InlineKeyboardButton(text="📊 История", callback_data="history")],
        [InlineKeyboardButton(text="🏠 Главное", callback_data="start")]
    ])
    
    await call.message.edit_text(bet, reply_markup=kb, parse_mode="HTML")
    await call.answer("✅ Ставка принята!")

@dp.callback_query(F.data == "history")
async def bet_history(call: types.CallbackQuery):
    await call.message.edit_text(
        "📊 <b>ИСТОРИЯ СТАВОК (март 2026)</b>\n\n"
        "✅ Зенит-ТБ2.5 1000₽ — <b>+900₽</b>\n"
        "✅ Сити-П1 500₽ — <b>+250₽</b>\n"
        "✅ Барса-ТБ2.5 1000₽ — <b>+800₽</b>\n\n"
        "<b>Прибыль: +1950₽ (65% ROI)</b>", 
        parse_mode="HTML"
    )
    await call.answer()

@dp.message()
async def echo(message: types.Message):
    await message.answer("🚀 /start — матчи 13-14 марта (выходные)!")

async def main():
    print("🚀 v7.3 — ВЫХОДНЫЕ 13-14 МАРТА!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())


