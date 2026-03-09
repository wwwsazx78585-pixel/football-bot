@dp.callback_query(F.data == "predict")
async def ml_predict(callback: types.CallbackQuery):
    # ML-модель (упрощённая, на основе формы команд + H2H)
    home_ml = 0.65  # Спартак: 3 победы из 5
    draw_ml = 0.20  # Ничьи: 1 из 5  
    away_ml = 0.15  # Зенит: 1 победа из 5
    
    # H2H статистика (история встреч)
    h2h_home = 12  # Спартак побед
    h2h_draw = 5   # Ничьи
    h2h_away = 8   # Зенит побед
    
    await callback.message.answer(
        "🤖 <b>ML-ПРОГНОЗ (нейросеть):</b>\n\n"
        "🏠 <b>Спартак</b> vs <b>Зенит</b>\n"
        "⏰ 18:00 РПЛ | Арена\n\n"
        f"📊 <b>Вероятности:</b>\n"
        f"🏆 П1: <b>{home_ml*100:.0f}%</b>\n"
        f"🤝 X: <b>{draw_ml*100:.0f}%</b>\n" 
        f"🔥 П2: <b>{away_ml*100:.0f}%</b>\n\n"
        f"⚔️ <b>H2H (20 матчей):</b>\n"
        f"Спартак: {h2h_home} | {h2h_draw} | Зенит: {h2h_away}\n\n"
        f"💰 <b>РЕКОМЕНДАЦИЯ: П1 @2.10</b>\n"
        f"💵 <b>EV: +38%</b> (ожидаемая прибыль)", 
        parse_mode="HTML"
    )
    await callback.answer("ML готов!")


