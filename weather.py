import httpx

LAT = 69.7008
LON = 170.3133
TIMEZONE = "Asia/Anadyr"


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


def wind_direction(deg):
    directions = [
        "⬆️ Северный",
        "↗️ Северо-восточный",
        "➡️ Восточный",
        "↘️ Юго-восточный",
        "⬇️ Южный",
        "↙️ Юго-западный",
        "⬅️ Западный",
        "↖️ Северо-западный",
    ]
    return directions[int((deg + 22.5) // 45) % 8]


async def get_weather():

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}"
        f"&longitude={LON}"
        "&current=temperature_2m,relative_humidity_2m,pressure_msl,"
        "weather_code,wind_speed_10m,wind_gusts_10m,wind_direction_10m"
        "&daily=temperature_2m_max,temperature_2m_min"
        f"&timezone={TIMEZONE}"
    )

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(url)
        response.raise_for_status()

    data = response.json()

    current = data["current"]
    daily = data["daily"]

    return {
        "temp_now": current["temperature_2m"],
        "temp_max": daily["temperature_2m_max"][0],
        "temp_min": daily["temperature_2m_min"][0],
        "humidity": current["relative_humidity_2m"],
        "pressure": current["pressure_msl"],
        "weather": WEATHER_CODES.get(
            current["weather_code"],
            "Неизвестно"
        ),
        "wind_speed": current["wind_speed_10m"],
        "wind_gust": current["wind_gusts_10m"],
        "wind_direction": wind_direction(
            current["wind_direction_10m"]
        ),
    }
