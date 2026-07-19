import os

from telegram import Bot

TOKEN = os.environ["TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


async def send_message(text):

    bot = Bot(TOKEN)

    await bot.send_message(
        chat_id=CHAT_ID,
        text=text
    )
