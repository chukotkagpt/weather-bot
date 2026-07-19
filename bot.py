import requests
import asyncio
from telegram import Bot
import os

TOKEN = os.environ["TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
API_KEY = os.environ["API_KEY"]


async def send_weather():
    url = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        "lat": 69.7008,
        "lon": 170.3133,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }

    r = requests.get(url, params=params)
    data = r.json()

    forecast = data["list"][0]

    temp = forecast["main"]["temp"]
    weather = forecast["weather"][0]["description"]
    wind_speed = forecast["wind"]["speed"]
    wind_deg = forecast["wind"]["deg"]
    gust = forecast["wind"].get("gust")
    pressure = forecast["main"]["pressure"]
    humidity = forecast["main"]["humidity"]
    clouds = forecast["clouds"]["all"]
    
        # Направление ветра
    if wind_deg >= 337.5 or wind_deg < 22.5:
        direction = "⬆️ Северный"
    elif wind_deg < 67.5:
        direction = "↗️ Северо-восточный"
    elif wind_deg < 112.5:
        direction = "➡️ Восточный"
    elif wind_deg < 157.5:
        direction = "↘️ Юго-восточный"
    elif wind_deg < 202.5:
        direction = "⬇️ Южный"
    elif wind_deg < 247.5:
        direction = "↙️ Юго-западный"
    elif wind_deg < 292.5:
        direction = "⬅️ Западный"
    else:
        direction = "↖️ Северо-западный"

    # Предупреждения
    warning = ""

    if "снег" in weather.lower():
        warning += "❄️ Возможен снегопад.\n"

    if wind_speed >= 15:
        warning += "🌬 Сильный ветер.\n"

    if wind_speed >= 25:
        warning += "🚨 Штормовой ветер!\n"

    if temp <= -30:
        warning += "🥶 Очень сильный мороз.\n"

    if "гололед" in weather.lower() or "ледяной" in weather.lower():
        warning += "🧊 Возможен гололёд.\n"

    # Расчёт прогноза клёва гольца
    score = 50

    if -5 <= temp <= 10:
        score += 20

    if wind_speed <= 5:
        score += 20
    elif wind_speed <= 10:
        score += 10
    else:
        score -= 10

    if clouds >= 50:
        score += 10

    score = max(0, min(score, 100))

    if score >= 80:
        fish = "🟢 Отличный"
    elif score >= 60:
        fish = "🟡 Хороший"
    elif score >= 40:
        fish = "🟠 Средний"
    else:
        fish = "🔴 Слабый"
        
    text = (
        f"🌅 Доброе утро!\n\n"
        f"📍 Певек\n"
        f"🌡 Температура: {temp:.1f}°C\n"
        f"☁️ {weather.capitalize()}\n"
        f"💨 Ветер: {wind_speed:.1f} м/с\n"
        f"{'🌬 Порывы: ' + str(round(gust, 1)) + ' м/с\n' if gust else ''}"
        f"🧭 Направление: {direction}\n\n"
        f"🎣 Клёв гольца: {fish} ({score}/100)\n\n"
        f"{warning if warning else '✅ Опасных погодных явлений не ожидается.'}"
    )

    bot = Bot(TOKEN)
    await bot.send_message(
        chat_id=CHAT_ID,
        text=text
    )


if __name__ == "__main__":
    asyncio.run(send_weather())
