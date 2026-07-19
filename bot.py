
import os
import asyncio
import requests
from telegram import Bot

TOKEN = os.environ["TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
API_KEY = os.environ["API_KEY"]
CITY = "Pevek"

async def send_weather():
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": CITY,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }

    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()

    wind_speed = data["wind"]["speed"]
    wind_deg = data["wind"].get("deg", 0)
    gust = data["wind"].get("gust")
    temp = data["main"]["temp"]
    clouds = data["clouds"]["all"]
    weather = data["weather"][0]["description"].lower()

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

    warning = ""
    if "снег" in weather:
        warning += "❄️ Сегодня ожидается снег.\n"
    if wind_speed >= 15:
        warning += "🌬 Сильный ветер.\n"
    if wind_speed >= 25:
        warning += "🚨 Штормовой ветер!\n"
    if temp <= -30:
        warning += "🥶 Сильный мороз.\n"
    if "гололед" in weather or "ледяной" in weather:
        warning += "🧊 Возможен гололёд.\n"

    score = 0
    if wind_speed <= 5:
        score += 25
    elif wind_speed <= 10:
        score += 15

    if -15 <= temp <= 10:
        score += 20

    if 1005 <= pressure <= 1025:
        score += 20

    if clouds >= 50:
        score += 15
    else:
        score += 5

    if humidity >= 70:
        score += 10

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
        f"📍 {data['name']}\n"
        f"🌡 Температура: {temp}°C\n"
        f"☁️ {data['weather'][0]['description'].capitalize()}\n"
        f"💨 Ветер: {wind_speed} м/с\n"
        f"{'🌬 Порывы: ' + str(gust) + ' м/с\n' if gust else ''}"
        f"🧭 Направление: {direction}\n"
        f"🎣 Клёв гольца: {fish} ({score}/100)\n\n"
        f"{warning}"
    )

    bot = Bot(TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=text)

if __name__ == "__main__":
    asyncio.run(send_weather())
