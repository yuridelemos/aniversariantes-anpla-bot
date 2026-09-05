import json
import os
from dotenv import load_dotenv
import requests

from src.data.drive_bot import DriveBot
from src.data.transform_dataframe import transform_dataframe
from src.visualization.visualize import barv_aniversariantes_by

load_dotenv()

TOKEN = os.getenv("API_KEY")

class TelegramBot:
    def __init__(self):
        self.token = TOKEN
        self.base_url = f"https://api.telegram.org/bot{self.token}/"
        self.driveBot = DriveBot()

    def start(self):
        update_id = None
        while True:
            updates = self.get_message(update_id)
            messages = updates["result"]
            if messages:
                for message in messages:
                    try:
                        update_id = message['update_id']
                        chat_id = message['message']['from']['id']
                        text = message['message']['text']
                        answer_bot, figure_boolean = self.create_answer(text)
                        self.send_answer(chat_id, answer_bot, figure_boolean)
                    except Exception as e:
                        print(f"Erro ao processar mensagem: {e}")


    def get_message(self, update_id):
        url = f"{self.base_url}getUpdates?timeout=1000"
        if update_id:
            url = f"{self.base_url}getUpdates?timeout=1000&offset={update_id + 1}"
        response = requests.get(url)
        return json.loads(response.content)

    def create_answer(self, message_text):
        dataframe = transform_dataframe(self.driveBot.get_data())
        message_text = message_text.lower()
        if message_text in ["/start", "ola", "eae", "menu", "oi", "oie", "iniciar", "iniciar bot", "start", "inicio", "começar", "comecar", "Oi"]:
            return """Seja bem vindo ao Bot de Aniversariantes da ANPLA Corretora. Selecione o que deseja:\n
                    1 - Aniversariantes do dia\n
                    2 - Quantidade de clientes por faixa etária\n
                    3 - Número de aniversiantes mensais\n""", 0 # 0 significa não enviar imagem, 1 significa enviar imagem
        elif message_text == '1':
            return "Não feito ainda", 0 # 0 significa não enviar imagem, 1 significa enviar imagem
        elif message_text == '2':
            return barv_aniversariantes_by(dataframe, "Mes"), 1 # 0 significa não enviar imagem, 1 significa enviar imagem
        elif message_text == '3':
            return barv_aniversariantes_by(dataframe, "Faixa Etária"), 1 # 0 significa não enviar imagem, 1 significa enviar imagem
        else:
            return """Comando não encontrado, tente novamente. Selecione o que deseja:\n
                    1 - Aniversariantes do dia\n
                    2 - Quantidade de clientes por faixa etária\n
                    3 - Número de aniversiantes mensais\n""", 0 # 0 significa não enviar imagem, 1 significa enviar imagem
    
    def send_answer(self, chat_id, answer, figure_boolean):
        if figure_boolean == 0:
            link_to_send = f"{self.base_url}sendMessage?chat_id={chat_id}&text={answer}"
            requests.get(link_to_send)
            return
        else:
            answer.seek(0)
            requests.post(f"{self.base_url}sendPhoto?chat_id={chat_id}", files=dict(photo=answer))
            answer.close()
            return