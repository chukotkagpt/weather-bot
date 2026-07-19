import requests
import asyncio
import schedule
import time
from telegram import Bot

import os

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

    r = requests.get(url, params=params)
    data = r.json()

    # Направление ветра
    wind_deg = data["wind"]["deg"]

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

    # Порывы ветра
    gust = data["wind"].get("gust")

    # Предупреждения
    weather = data["weather"][0]["description"].lower()
    warning = ""

    if "снег" in weather:
        warning += "❄️ Внимание! Сегодня ожидается снегопад.\n"

    if data["wind"]["speed"] >= 15:
        warning += "🌬 Внимание! Сильный ветер.\n"

    if data["wind"]["speed"] >= 25:
        warning += "🚨 Штормовой ветер! Будьте осторожны.\n"

    if data["main"]["temp"] <= -30:
        warning += "🥶 Внимание! Сильный мороз.\n"

    if "ледяной" in weather or "гололед" in weather:
        warning += "🧊 Осторожно! Возможен гололёд.\n"

    # Сообщение
    text = (
        f"🌅 Доброе утро!\n\n"
        f"📍 {data['name']}\n"
        f"🌡 Температура: {data['main']['temp']}°C\n"
        f"☁️ {data['weather'][0]['description'].capitalize()}\n"
        f"💨 Ветер: {data['wind']['speed']} м/с\n"
        f"{'🌬 Порывы: ' + str(gust) + ' м/с\n' if gust else ''}"
        f"🧭 Направление: {direction}\n"
        f"\n{warning}"
    )

    bot = Bot(TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=text)


def job():
    asyncio.run(send_weather())


# Проверка сразу после запуска
job()

# Ежедневная отправка
schedule.every().day.at("08:00").do(job)

print("✅ Бот запущен и ожидает 08:00...")

while True:
    schedule.run_pending()
    time.sleep(30)