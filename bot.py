import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔥 Открыть R1",
                url="https://zxcr1mty.github.io/R1/"
            )
        ]
    ])

    await message.answer(
        "<b>R1</b>\n\nНажми кнопку ниже, чтобы открыть сайт 👇",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
