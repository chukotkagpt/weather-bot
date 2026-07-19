import os
import asyncio
import httpx
from telegram import Bot

# ==========================
# Telegram
# ==========================

TOKEN = os.environ["TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# ==========================
# Open-Meteo
# ==========================

LAT = 69.7008
LON = 170.3133
TIMEZONE = "Asia/Anadyr"

# ==========================
# TidesAtlas
# ==========================

TIDES_API_KEY = os.environ["TIDES_API_KEY"]

# ==========================
# Описание погодных кодов
# ==========================

WEATHER_CODES = {
    0: "☀️ Ясно",
    1: "🌤 Преимущественно ясно",
    2: "⛅ Переменная облачность",
    3: "☁️ Пасмурно",
    45: "🌫 Туман",
    48: "🌫 Изморозь",
    51: "🌦 Морось",
    53: "🌦 Морось",
    55: "🌧 Сильная морось",
    61: "🌧 Дождь",
    63: "🌧 Дождь",
    65: "🌧 Ливень",
    71: "🌨 Небольшой снег",
    73: "❄️ Снег",
    75: "❄️ Сильный снег",
    77: "🌨 Снежная крупа",
    80: "🌦 Ливневый дождь",
    81: "🌧 Сильный ливень",
    82: "⛈ Очень сильный ливень",
    85: "🌨 Снегопад",
    86: "❄️ Сильный снегопад",
    95: "⛈ Гроза",
    96: "⛈ Гроза с градом",
    99: "⛈ Сильная гроза",
}
    
    # ==========================
# Получение погоды Open-Meteo
# ==========================
# ==========================
# Направление ветра
# ==========================

def wind_direction(deg):

    directions = [
        "⬆️ Северный",
        "↗️ Северо-восточный",
        "➡️ Восточный",
        "↘️ Юго-восточный",
        "⬇️ Южный",
        "↙️ Юго-западный",
        "⬅️ Западный",
        "↖️ Северо-западный"
    ]

    return directions[int((deg + 22.5) // 45) % 8]


# ==========================
# Получение погоды
# ==========================

async def get_weather():

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}"
        f"&longitude={LON}"
        "&current=temperature_2m,weather_code,wind_speed_10m,wind_gusts_10m,wind_direction_10m"
        "&daily=temperature_2m_max,temperature_2m_min,weather_code"
        f"&timezone={TIMEZONE}"
    )

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(url)
        response.raise_for_status()

    data = response.json()

    current = data["current"]
    daily = data["daily"]

    weather = {
        "temp_now": current["temperature_2m"],
        "temp_max": daily["temperature_2m_max"][0],
        "temp_min": daily["temperature_2m_min"][0],
        "weather_code": daily["weather_code"][0],
        "weather": WEATHER_CODES.get(
            daily["weather_code"][0],
            "🌍 Неизвестная погода"
        ),
        "wind_speed": current["wind_speed_10m"],
        "wind_gust": current["wind_gusts_10m"],
        "wind_deg": current["wind_direction_10m"],
        "wind_dir": wind_direction(current["wind_direction_10m"])
    }

    return weather

    async def get_tides():

    url = (
       "https://tidesatlas.com/api/v1/tides" 
        f"?lat={LAT}"
        f"&lon={LON}"
        "&days=1"
    )

    headers = {
        "X-API-Key": TIDES_API_KEY
    }

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()

    data = response.json() 
       extremes = data["extremes"]

high_tide = None
low_tide = None

for tide in extremes:
    if tide["type"] == "high" and high_tide is None:
        high_tide = tide

    if tide["type"] == "low" and low_tide is None:
        low_tide = tide

return {
    "high": high_tide,
    "low": low_tide
}
    # ==========================
# Предупреждения
# ==========================

def get_warnings(weather):

    warnings = []

    if weather["temp_min"] <= -30:
        warnings.append("🥶 Очень сильный мороз.")

    if weather["wind_speed"] >= 15:
        warnings.append("🌬 Сильный ветер.")

    if weather["wind_gust"] >= 20:
        warnings.append("🌪 Очень сильные порывы ветра.")

    if weather["weather_code"] in [71, 73, 75, 85, 86]:
        warnings.append("❄️ Ожидается снег.")

    if weather["weather_code"] in [95, 96, 99]:
        warnings.append("⛈ Возможна гроза.")

    return warnings
    
    # ==========================
# Прогноз клёва
# ==========================

def fish_forecast(weather):

    score = 50
    reasons = []

    # Температура
    if -5 <= weather["temp_now"] <= 8:
        score += 20
        reasons.append("✅ Комфортная температура")

    elif 8 < weather["temp_now"] <= 12:
        score += 10
        reasons.append("✅ Подходящая температура")

    elif weather["temp_now"] > 15:
        score -= 15
        reasons.append("⚠️ Слишком тепло")

    # Ветер
    if weather["wind_speed"] <= 5:
        score += 20
        reasons.append("✅ Слабый ветер")

    elif weather["wind_speed"] <= 10:
        score += 10
        reasons.append("✅ Умеренный ветер")

    elif weather["wind_speed"] >= 15:
        score -= 20
        reasons.append("⚠️ Сильный ветер")

    # Порывы
    if weather["wind_gust"] >= 20:
        score -= 15
        reasons.append("⚠️ Сильные порывы")

    # Пасмурная погода
    if weather["weather_code"] in [2, 3]:
        score += 10
        reasons.append("✅ Пасмурная погода")

    score = max(0, min(score, 100))

    if score >= 80:
        level = "🟢 Отличный"
        best_time = "06:00–10:00"

    elif score >= 60:
        level = "🟡 Хороший"
        best_time = "07:00–10:00"

    elif score >= 40:
        level = "🟠 Средний"
        best_time = "08:00–10:00"

    else:
        level = "🔴 Слабый"
        best_time = "Хорошего времени не ожидается"

    return score, level, best_time, reasons
    
    # ==========================
# Отправка сообщения
# ==========================

async def send_weather():

    weather = await get_weather()

    warnings = get_warnings(weather)

    score, level, best_time, reasons = fish_forecast(weather)

    text = (
        f"🌅 Доброе утро!\n\n"
        f"📍 Певек\n\n"
        f"🌡 Сейчас: {weather['temp_now']:.1f}°C\n"
        f"📈 Днём: {weather['temp_max']:.1f}°C\n"
        f"📉 Ночью: {weather['temp_min']:.1f}°C\n\n"
        f"{weather['weather']}\n\n"
        f"💨 Ветер: {weather['wind_speed']:.1f} м/с\n"
        f"🌬 Порывы: {weather['wind_gust']:.1f} м/с\n"
        f"🧭 Направление: {weather['wind_dir']}\n\n"
        f"🎣 Морской голец\n"
        f"{level} ({score}/100)\n\n"
    )

    if reasons:
        text += "Причины:\n"
        for reason in reasons:
            text += f"{reason}\n"

    text += f"\n⏰ Лучшее время:\n{best_time}\n"

    if warnings:
        text += "\n⚠️ Предупреждения:\n"
        for warning in warnings:
            text += f"• {warning}\n"
    else:
        text += "\n✅ Опасных погодных явлений не ожидается."

    bot = Bot(TOKEN)

    await bot.send_message(
        chat_id=CHAT_ID,
        text=text
    )


async def main():
    await send_weather()


if __name__ == "__main__":
    asyncio.run(main())
