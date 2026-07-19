def fish_forecast(weather, tides=None):

    score = 50
    reasons = []

    # Температура
    if 4 <= weather["temp_now"] <= 12:
        score += 15
        reasons.append("✅ Подходящая температура")
    elif weather["temp_now"] > 18:
        score -= 15
        reasons.append("❌ Слишком тепло")

    # Давление
if 1008 <= weather["pressure"] <= 1022:
    score += 8

elif weather["pressure"] < 995:
    score -= 10

# Влажность
if weather["humidity"] > 80:
    score += 3

elif weather["humidity"] < 45:
    score -= 3

# Скорость ветра
if 2 <= weather["wind_speed"] <= 7:
    score += 15
    reasons.append("✅ Умеренный ветер")

elif weather["wind_speed"] > 12:
    score -= 20
    reasons.append("❌ Сильный ветер")

    # Порывы
    if weather["wind_gust"] > 15:
        score -= 15
        reasons.append("❌ Сильные порывы")

    # Пасмурная погода
    if "☁️" in weather["weather"] or "🌦" in weather["weather"]:
        score += 10
        reasons.append("✅ Пасмурная погода")

    # Приливы (будут работать после подключения tides.py)
    if tides:
        if tides.get("state") == "rising":
            score += 15
            reasons.append("🌊 Идёт прилив")

        elif tides.get("state") == "high":
            score += 10
            reasons.append("🌊 Полная вода")

        elif tides.get("state") == "falling":
            score -= 5
            reasons.append("🌊 Начался отлив")

    # Ограничиваем диапазон
    score = max(0, min(score, 100))

    # Оценка
    if score >= 85:
        level = "🟢 Отличный"

    elif score >= 70:
        level = "🟡 Хороший"

    elif score >= 50:
        level = "🟠 Средний"

    else:
        level = "🔴 Плохой"

    # Лучшее время
    if score >= 70:
        best_time = "06:00–10:00\n18:00–22:00"
    else:
        best_time = "Клёв маловероятен"

    # Формируем сообщение
    text = (
        f"🌅 Доброе утро!\n\n"
        f"📍 Певек\n\n"
        f"🌡 Сейчас: {weather['temp_now']:.1f}°C\n"
        f"📈 Днём: {weather['temp_max']:.1f}°C\n"
        f"📉 Ночью: {weather['temp_min']:.1f}°C\n\n"
        f"{weather['weather']}\n\n"
        f"💨 Ветер: {weather['wind_speed']:.1f} м/с\n"
        f"🌬 Порывы: {weather['wind_gust']:.1f} м/с\n"
        f"🧭 Направление: {weather['wind_direction']}\n\n"
        f"🎣 Морской голец\n"
        f"{level} ({score}/100)\n\n"
    )

    if reasons:
        text += "Причины:\n"
        for reason in reasons:
            text += f"{reason}\n"

    text += f"\n⏰ Лучшее время:\n{best_time}"

    return text
