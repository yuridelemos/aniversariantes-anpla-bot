import asyncio
import os
from flask import Flask, request, abort
from dotenv import load_dotenv

from src.telegram_bot import TelegramBot

load_dotenv()

app = Flask(__name__)
bot = TelegramBot()

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")  # string aleatória que só você e o Telegram sabem
if not WEBHOOK_SECRET:
    raise RuntimeError("Variável de ambiente WEBHOOK_SECRET não foi definida.")

@app.route("/webhook", methods=["POST"])
def webhook():
    # Confirma que a requisição realmente veio do Telegram
    token_recebido = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if token_recebido != WEBHOOK_SECRET:
        abort(403)

    update = request.get_json(force=True)
    asyncio.run(bot.process_update(update))
    return "ok", 200


@app.route("/")
def health_check():
    return "Bot está no ar!", 200