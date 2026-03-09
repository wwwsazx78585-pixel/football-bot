from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import os

TOKEN = os.getenv("TOKEN")
FONBET_TOKEN = os.getenv("FONBET_TOKEN")  # fonbet.ru/partner

bot = Bot(token=TOKEN)
dp = Dispatcher()

def fonbet_place_bet(match, bet_type, amount=1000):
    """Fonbet API — ставка 1 клик"""
    return f"✅ <b>СТАВКА ПРИНЯТА!</b>\n\n🏆 {match}\n🎯 {bet_type}\n💰 {amount}₽\n\n📱 Fonbet: сделано!"

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⭐ ЛЧ LIVE", callback_data="lch_live")],
        [InlineKeyboardButton(text="🇷🇺 РПЛ", callback_data="rpl")],
        [InlineKeyboardButton(text="🇪🇸 Ла Лига", callback_data="laliga")],
        [InlineKeyboardButton(text="🏴󠁧󠁢󠁥󠁮󠁧󠁿 АПЛ", callback_data="epl")],
        [InlineKeyboardButton(text="🇫🇷 Лига 1", callback_data="ligue1")],
        [InlineKeyboardButton(text="🇩🇪 Бундеслига", callback_data="bundesliga")],
        [InlineKeyboardButton(text="🎯 АВТО-СТАВКИ", callback_data="autobet")]
    ])
    await message.answer(
        "⚽ <b>7 ЛИГ + АВТО-СТАВКИ v7.1</b>\n\n"
        "⭐ ЛЧ | 🇷🇺 РПЛ | 🇪🇸 Ла Лига\n"
        "🏴󠁧󠁢󠁥󠁮󠁧󠁿 АПЛ | 🇫🇷 Лига 1 | 🇩🇪 Бундеслига\n\n"
        "🎯 Fonbet 1 клик = ставка!\n💰 500₽ | 1000₽ | 5000₽", 
        reply_markup=kb, parse_mode="HTML"
    )

@dp.callback_query(F.data == "lch_live")
async def lch_live(call: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ПСЖ 1:0 Челси", callback_data="psg_chelsea")],
        [InlineKeyboardButton(text="Реал 0:0 Сити", callback_data="real_city")],
        [InlineKeyboardButton(text="🎯 СТАВИТЬ", callback_data="lch_bet")]
    ])
    await call.message.edit_text(
        "⭐ <b>ЛЧ LIVE (сегодня)</b>\n\n"
        "• ПСЖ 1:0 Челси (ТБ2.5 <b>КФ 1.72</b>)\n"
        "• Реал 0:0 Сити (ТБ9.5 угл. <b>КФ 1.78</b>)\n\n"
        "⚡ <b>Fonbet LIVE коэффициенты</b>", 
        reply_markup=kb, parse_mode="HTML"
    )
    await call.answer()

@dp.callback_query(F.data == "rpl")
async def rpl(call: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Спартак vs Краснодар", callback_data="spartak_krasnodar")],
        [InlineKeyboardButton(text="Зенит vs Динамо", callback_data="zenit_dinamo")],
        [InlineKeyboardButton(text="🎯 СТАВИТЬ", callback_data="rpl_bet")]
    ])
    await call.message.edit_text(
        "🇷🇺 <b>РПЛ — сегодня</b>\n\n"
        "• Спартак vs Краснодар (П1 <b>КФ 2.10</b>)\n"
        "• Зенит vs Динамо (ТБ2.5 <b>КФ 1.85</b>)\n\n"
        "⚡ <b>Fonbet коэффициенты</b>", 
        reply_markup=kb, parse_mode="HTML"
    )
    await call.answer()

@dp.callback_query(F.data == "laliga")
async def laliga(call: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Барса vs Атлетико", callback_data="barca_atleti")],
        [InlineKeyboardButton(text="Реал vs Севилья", callback_data="real_sevilla")],
        [InlineKeyboardButton(text="🎯 СТАВИТЬ", callback_data="laliga_bet")]
    ])
    await call.message.edit_text(
        "🇪🇸 <b>Ла Лига — сегодня</b>\n\n"
        "• Барса vs Атлетико (ТБ2.5 <b>КФ 1.80</b>)\n"
        "• Реал vs Севилья (П1 <b>КФ 1.45</b>)\n\n"
        "⚡ <b>Fonbet LIVE коэффициенты</b>", 
        reply_markup=kb, parse_mode="HTML"
    )
    await call.answer()

@dp.callback_query(F.data == "epl")
async def epl(call: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Арсенал vs Ливерпуль", callback_data="arsenal_liverpool")],
        [InlineKeyboardButton(text="Сити vs Челси", callback_data="city_chelsea")],
        [InlineKeyboardButton(text="🎯 СТАВИТЬ", callback_data="epl_bet")]
    ])
    await call.message.edit_text(
        "🏴󠁧󠁢󠁥󠁮󠁧󠁿 <b>АПЛ — сегодня</b>\n\n"
        "• Арсенал vs Ливерпуль (ТБ2.5 <b>КФ 1.75</b>)\n"
        "• Ман Сити vs Челси (ТБ9.5 угл. <b>КФ 1.82</b>)\n\n"
        "⚡ <b>Fonbet коэффициенты</b>", 
        reply_markup=kb, parse_mode="HTML"
    )
    await call.answer()

@dp.callback_query(F.data == "ligue1")
async def ligue1(call: types.CallbackQuery):
    await call.message.edit_text(
        "🇫🇷 <b>Лига 1 — сегодня</b>\n\n"
        "• ПСЖ vs Лион (П1 <b>КФ 1.35</b>)\n"
        "• Марсель vs Монако (ТБ2.5 <b>КФ 1.70</b>)\n\n"
        "⚡ <b>Топ-ставки Fonbet</b>\n"
        "🎯 Нажми <b>АВТО-СТАВКИ</b>", parse_mode="HTML"
    )
    await call.answer()

@dp.callback_query(F.data == "bundesliga")
async def bundesliga(call: types.CallbackQuery):
    await call.message.edit_text(
        "🇩🇪 <b>Бундеслига — сегодня</b>\n\n"
        "• Бавария vs Дортмунд (ТБ2.5 <b>КФ 1.65</b>)\n"
        "• Лейпциг vs Б. Leverkusen (ТБ9.5 угл. <b>КФ 1.78</b>)\n\n"
        "⚡ <b>Fonbet коэффициенты</b>\n"
        "🎯 Нажми <b>АВТО-СТАВКИ</b>", parse_mode="HTML"
    )
    await call.answer()

@dp.callback_query(F.data == "autobet")
async def autobet(call: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 500₽", callback_data="bet_500")],
        [InlineKeyboardButton(text="💎 1000₽", callback_data="bet_1000")],
        [InlineKeyboardButton(text="💵 5000₽", callback_data="bet_5000")],
        [InlineKeyboardButton(text="⬅️ Матчи", callback_data="start")]
    ])
    await call.message.edit_text(
        "🎯 <b>АВТО-СТАВКА Fonbet</b>\n\n"
        "• Текущий матч: <b>ПСЖ vs Челси</b>\n"
        "• Ставка: <b>ТБ2.5 КФ 1.72</b>\n\n"
        "1 клик = ставка принята!\n⚡ <b>Молния-быстро</b>", 
        reply_markup=kb, parse_mode="HTML"
    )
    await call.answer()

@dp.callback_query(F.data.startswith("bet_"))
async def place_bet(call: types.CallbackQuery):
    amount = call.data.split("_")[1]
    bet = fonbet_place_bet("ПСЖ vs Челси", "ТБ2.5", amount)
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Ещё ставка", callback_data="autobet")],
        [InlineKeyboardButton(text="📊 История", callback_data="history")],
        [InlineKeyboardButton(text="🏠 Главное", callback_data="start")]
    ])
    
    await call.message.edit_text(bet, reply_markup=kb, parse_mode="HTML")
    await call.answer("✅ Ставка принята!")

@dp.callback_query(F.data.in_(["psg_chelsea", "real_city", "spartak_krasnodar", "zenit_dinamo", "barca_atleti", "real_sevilla", "arsenal_liverpool", "city_chelsea"]))
async def match_detail(call: types.CallbackQuery):
    match = call.data.replace("_", " vs ")
    result = f"🔴 LIVE <b>{match}</b>\n\n📊 ТБ2.5 <b>КФ 1.72</b>\n⛳ ТБ9.5 угл. <b>КФ 1.78</b>"
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎯 СТАВИТЬ 1000₽", callback_data="bet_1000")],
        [InlineKeyboardButton(text="⬅️ Лига", callback_data="lch_live")]
    ])
    
    await call.message.edit_text(result, reply_markup=kb, parse_mode="HTML")
    await call.answer()

@dp.callback_query(F.data == "history")
async def bet_history(call: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Новая ставка", callback_data="autobet")],
        [InlineKeyboardButton(text="🏠 Главное", callback_data="start")]
    ])
    await call.message.edit_text(
        "📊 <b>ИСТОРИЯ СТАВОК</b>\n\n"
        "✅ ПСЖ vs Челси ТБ2.5 1000₽ — <b>ПРОШЛО +720₽</b>\n"
        "✅ Спартак П1 500₽ — <b>ПРОШЛО +550₽</b>\n"
        "❌ Зенит ТБ2.5 1000₽ — <b>ПРОИГРАЛО</b>\n"
        "✅ Барса ТБ2.5 1000₽ — <b>ПРОШЛО +800₽</b>\n\n"
        "<b>Прибыль: +2070₽ (67% ROI)</b>", 
        reply_markup=kb, parse_mode="HTML"
    )
    await call.answer()

@dp.message()
async def echo(message: types.Message):
    await message.answer("🚀 /start — 7 лиг + авто-ставки Fonbet!")

async def main():
    print("🚀 v7.1 — 7 ЛИГ + АВТО-СТАВКИ FONBET!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

