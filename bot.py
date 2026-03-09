import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.handlers import CallbackQueryHandler

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("🚫 TOKEN не найден!")

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
        "⚽ <b>ФУТБОЛЬНЫЙ БОТ</b>\n\n"
        "✅ <b>КНОПКИ РАБОТАЮТ!</b>\n"
        "Нажми любую:", 
        reply_markup=keyboard, 
        parse_mode="HTML"
    )

# 🔥 ОБРАБОТЧИКИ КНОПОК
@dp.callback_query(F.data == "today")
async def process_today(callback: types.CallbackQuery):
    await callback.message.answer("⚽ Сегодня РПЛ:\n• Спартак vs Зенит (18:00)\n• Динамо vs Локо (20:00)")
    await callback.answer()  # Убирает "часики"

@dp.callback_query(F.data == "predict")
async def process_predict(callback: types.CallbackQuery):
    await callback.message.answer(
        "🔮 <b>ПРОГНОЗ ДНЯ:</b>\n\n"
        "🏠 <b>Спартак</b> 2:1 <b>Зенит</b>\n"
        "⏰ 18:00, РПЛ\n\n"
        "💰 <b>Ставка: П1 (2.10)</b>", 
        parse_mode="HTML"
    )
    await callback.answer()

@dp.callback_query(F.data == "leagues")
async def process_leagues(callback: types.CallbackQuery):
    await callback.message.answer(
        "📊 <b>ТОП-ЛИГИ:</b>\n\n"
        "⚽ <b>РПЛ</b> - Россия\n"
        "🏴󠁧󠁢󠁥󠁮󠁧󠁿 <b>АПЛ</b> - Англия\n"
        "🇪🇸 <b>Ла Лига</b> - Испания\n"
        "🇮🇹 <b>Серия А</b> - Италия", 
        parse_mode="HTML"
    )
    await callback.answer()

@dp.message(Command("predict"))
async def cmd_predict(message: types.Message):
    await message.answer(
        "🔮 <b>ПРОГНОЗ:</b>\n"
        "🏠 Спартак 2:1 Зенит\n"
        "💰 Ставка: П1 (2.10)", 
        parse_mode="HTML"
    )

@dp.message()
async def echo(message: types.Message):
    await message.answer("📱 /start — меню с кнопками")

async def main():
    print("🚀 Бот с РАБОЧИМИ КНОПКАМИ запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
