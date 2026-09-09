import json
import os
from dotenv import load_dotenv
import requests
from telegram import Bot, Update
from telegram.ext import ContextTypes

from src.data.aniversariantes import aniversariantes_do_dia
from src.data.drive_bot import DriveBot
from src.data.transform_dataframe import transform_dataframe
from src.visualization.visualize import barv_aniversariantes_by

load_dotenv()

TOKEN = os.getenv("API_KEY")
if not TOKEN:
    raise RuntimeError("Variável de ambiente API_KEY não foi definida.")

COMANDOS_INICIO = {
    "/start", "ola", "eae", "menu", "oi", "oie",
    "iniciar", "iniciar bot", "start", "inicio", "começar", "comecar"
}

MENU_TEXTO = (
    "Seja bem vindo ao Bot de Aniversariantes da ANPLA Corretora. "
    "Selecione o que deseja:\n\n"
    "1 - Aniversariantes do dia\n"
    "2 - Quantidade de clientes por faixa etária\n"
    "3 - Número de aniversariantes mensais\n"
)


class TelegramBot:
    def __init__(self):
        self.token = TOKEN
        self.base_url = f"https://api.telegram.org/bot{self.token}/"
        self.driveBot = DriveBot()
        self.session = requests.Session()
        self.allowed_user_ids = {
            int(user_id.strip())
            for user_id in os.getenv(
                "TELEGRAM_ALLOWED_USER_IDS",
                ""
            ).split(",")
            if user_id.strip()
        }

        self.bot = Bot(token=self.token)

    def is_authorized(self, update: Update) -> bool:
        user = update.effective_user

        if user is None:
            return False

        return user.id in self.allowed_user_ids

    async def restrict_access(self, update: Update) -> bool:
        if self.is_authorized(update):
            return True

        if update.message:
            await update.message.reply_text("🚫 Você não tem autorização para usar este bot.")
        return False

    async def process_update(self, update: dict):
        """Processa uma única atualização vinda do webhook do Telegram."""
        try:
            message = update["message"]
            chat_id = message["chat"]["id"]
            text = message["text"]
        except KeyError:
            return  # mensagem sem texto (sticker, foto, etc.) — ignora

        try:
            telegram_update = Update.de_json(update, self.bot)

            if not await self.restrict_access(telegram_update):
                return

            answer_bot, is_photo = self.create_answer(text)
            self.send_answer(chat_id, answer_bot, is_photo)
        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")

    def create_answer(self, message_text):
        message_text = message_text.strip().lower()

        if message_text in COMANDOS_INICIO:
            return MENU_TEXTO, False

        if message_text == '1':
            dataframe = transform_dataframe(self.driveBot.get_data())
            hoje_df = aniversariantes_do_dia(dataframe)
            if hoje_df.empty:
                return "Não há aniversariantes hoje.", False
            nomes = "\n".join(
                f'{row["Nome"]} - {row["Data de Nascimento"].strftime("%d/%m/%Y")} - {row["Idade"]} anos - {row["Ramo"]} - {row["Observacao"]}' for _, row in hoje_df.iterrows())
            return f"🎂 Aniversariantes de hoje:\n\n{nomes}", False

        if message_text in ('2', '3'):
            dataframe = transform_dataframe(self.driveBot.get_data())
            eixo = "Mes" if message_text == '2' else "Faixa Etária"
            return barv_aniversariantes_by(dataframe, eixo), True

        return f"Comando não encontrado, tente novamente.\n\n{MENU_TEXTO}", False

    def send_answer(self, chat_id, answer, is_photo):
        if not is_photo:
            self.session.get(
                f"{self.base_url}sendMessage",
                params={"chat_id": chat_id, "text": answer}
            )
            return

        answer.seek(0)
        self.session.post(
            f"{self.base_url}sendPhoto",
            params={"chat_id": chat_id},
            files={"photo": answer}
        )
        answer.close()