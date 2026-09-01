from flask import Flask, request
import os
import requests

app = Flask(__name__)

# Токен из переменной окружения (на Render)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Токен не найден! Добавь TELEGRAM_BOT_TOKEN в переменные окружения.")

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

STEAM_ID = "1596319409"
LAUNCH_OPTIONS = "+exec autoexec.cfg -language russian -novr -dx11 -nohltv -noaafonts -processheap -noborder -novid -console -map dota -nohltv -prewarm"
AUTOEXEC = """dota_minimap_creep_scale 1.7
dota_minimap_rune_size 700
fps_max 0
dota_unit_use_player_color 1
dota_friendly_color 0 255 0
dota_enemy_color 0 0 255
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

def send_message(chat_id, text, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(f"{TELEGRAM_API}/sendMessage", json=payload)

def get_main_keyboard():
    return {
        "inline_keyboard": [
            [{"text": "STRATZ", "url": f"https://stratz.com/players/{STEAM_ID}"}],
            [{"text": "Dotabuff", "url": f"https://ru.dotabuff.com/players/{STEAM_ID}"}],
            [{"text": "OpenDota", "url": f"https://www.opendota.com/players/{STEAM_ID}"}],
            [{"text": "Параметры запуска", "callback_data": "launch"}],
            [{"text": "Autoexec.cfg", "callback_data": "autoexec"}],
            [{"text": "Мои бинды", "callback_data": "binds"}],
            [{"text": "Открыть сайт", "url": "https://zxcr1mty.github.io/R1/"}],
        ]
    }

@app.route('/')
def home():
    return "Bot is running!", 200

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    update = request.get_json()
    if "message" in update:
        msg = update["message"]
        chat_id = msg["chat"]["id"]
        
        if msg.get("text") == "/start":
            text = "<b>R1 | Dota 2 Settings</b>\n\nПривет! Выбирай, куда перейти: 👇"
            send_message(chat_id, text, get_main_keyboard())
    
    elif "callback_query" in update:
        call = update["callback_query"]
        chat_id = call["message"]["chat"]["id"]
        
        if call["data"] == "launch":
            text = f"<b>Параметры запуска:</b>\n<code>{LAUNCH_OPTIONS}</code>"
            send_message(chat_id, text, get_main_keyboard())
        elif call["data"] == "autoexec":
            text = f"<b>Autoexec.cfg:</b>\n<code>{AUTOEXEC}</code>"
            send_message(chat_id, text, get_main_keyboard())
        elif call["data"] == "binds":
            binds_text = ""
            for key, command in BINDS.items():
                binds_text += f"<code>{key}</code> → {command}\n"
            text = f"<b>Мои бинды:</b>\n{binds_text}"
            send_message(chat_id, text, get_main_keyboard())
        
        requests.post(f"{TELEGRAM_API}/answerCallbackQuery", json={"callback_query_id": call["id"]})

    return "ok", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
