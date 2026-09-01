import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# Токен берём из переменной окружения (Railway/сервер)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Ошибка: токен не найден. Добавь переменную TELEGRAM_BOT_TOKEN!")

# Твои данные
STEAM_ID = "1596319409"
LAUNCH_OPTIONS = "+exec autoexec.cfg -language russian -novr -dx11 -nohltv -noaafonts -processheap -noborder -novid -console -map dota -nohltv -prewarm"
AUTOEXEC = """dota_minimap_creep_scale 1.7
dota_minimap_rune_size 700
fps_max 0
dota_unit_use_player_color 1;
dota_friendly_color 0 255 0;
dota_enemy_color 0 0 255;
map_enable_portrait_worlds 1
-nojoy
-high
-noaafonts
-dxlevel 100
-heapsize 2097152"""

BINDS = {
    "Мышь 4": "Выбрать героя",
    "Alt-Мышь 5": "Выбрать всех своих существ",
    "CAPSLOCK": "Следующее существо",
    "TAB": "1-я группа",
    "Alt-Мышь 4": "3-я группа",
    "5": "5-я группа",
    "Мышь 5": "6-я группа",
}

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Главное меню
def get_main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="STRATZ", url=f"https://stratz.com/players/{STEAM_ID}")],
        [InlineKeyboardButton(text="Dotabuff", url=f"https://ru.dotabuff.com/players/{STEAM_ID}")],
        [InlineKeyboardButton(text="OpenDota", url=f"https://www.opendota.com/players/{STEAM_ID}")],
        [InlineKeyboardButton(text="Параметры запуска", callback_data="launch")],
        [InlineKeyboardButton(text="Autoexec.cfg", callback_data="autoexec")],
        [InlineKeyboardButton(text="Мои бинды", callback_data="binds")],
    ])

def format_message(text):
    return f"<b>R1 | Dota 2 Settings</b>\n\n{text}"

# Команда /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    text = format_message(
        "Привет! Это мой личный хаб с настройками Dota 2.\n"
        "Выбирай, что тебе нужно 👇"
    )
    await message.answer(text, reply_markup=get_main_keyboard(), parse_mode="HTML")

# Обработка нажатий на кнопки
@dp.callback_query()
async def handle_callbacks(call: CallbackQuery):
    if call.data == "launch":
        text = format_message(f"<b>Запуск:</b>\n<code>{LAUNCH_OPTIONS}</code>")
        await call.message.edit_text(text, reply_markup=get_main_keyboard(), parse_mode="HTML")
    
    elif call.data == "autoexec":
        text = format_message(f"<b>Autoexec.cfg:</b>\n<code>{AUTOEXEC}</code>")
        await call.message.edit_text(text, reply_markup=get_main_keyboard(), parse_mode="HTML")
    
    elif call.data == "binds":
        binds_text = ""
        for key, command in BINDS.items():
            binds_text += f"<code>{key}</code> → {command}\n"
        text = format_message(f"<b>Мои бинды:</b>\n{binds_text}")
        await call.message.edit_text(text, reply_markup=get_main_keyboard(), parse_mode="HTML")

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())