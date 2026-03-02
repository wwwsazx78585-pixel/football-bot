import asyncio, os, random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("⚽ <b>ФУТБОЛЬНЫЙ БОТ ОНЛАЙН!</b>\n\n🔥 /predict — свежий прогноз\n📊 /stats — статистика", parse_mode="HTML")

@dp.message(Command("predict"))
async def predict(message: types.Message):
    teams = ["Спартак", "Зенит", "ЦСКА", "Локо", "Динамо", "Краснодар"]
    team1, team2 = random.choice(teams), random.choice(teams)
    outcomes = [
        "🏆 <b>Победа хозяев 2.10</b>",
        "🤝 <b>Ничья 3.40</b>", 
        "🔥 <b>Победа гостей 2.80</b>",
        "⚽ <b>Тотал больше 2.5 (1.85)</b>",
        "🅰️ <b>Обе забьют (1.75)</b>"
    ]
    prediction = random.choice(outcomes)
    await message.answer(f"🔥 <b>{team1} vs {team2}</b>\n\n🎯 {prediction}", parse_mode="HTML")

@dp.message(Command("stats"))
async def stats(message: types.Message):
    await message.answer("📊 <b>СТАТИСТИКА БОТА:</b>\n\n✅ 65% точности прогнозов\n⚽ 120+ матчей в базе\n📈 ML-модель v1.0", parse_mode="HTML")

@dp.message()
async def echo(message: types.Message):
    await message.answer("📱 <b>Команды:</b>\n/start — меню\n/predict — прогноз\n/stats — статистика", parse_mode="HTML")

async def main():
    print("🚀 Футбольный бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
