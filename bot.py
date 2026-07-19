import asyncio

from weather import get_weather
from tides import get_tides
from fish import fish_forecast
from telegram_sender import send_message


async def main():
    weather = await get_weather()
    tides = await get_tides()

    message = fish_forecast(
        weather=weather,
        tides=tides
    )

    await send_message(message)


if __name__ == "__main__":
    asyncio.run(main())
