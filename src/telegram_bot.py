import json
import os
from dotenv import load_dotenv
import requests

load_dotenv()

TOKEN = os.getenv("API_KEY")

class TelegramBot:
    def __init__(self):
        self.token = TOKEN
        self.base_url = f"https://api.telegram.org/bot{self.token}/"

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
                        answer_bot = self.create_answer(text)
                        self.send_answer(chat_id, answer_bot)
                    except:
                        pass


    def get_message(self, update_id):
        url = f"{self.base_url}getUpdates?timeout=1000"
        if update_id:
            url = f"{self.base_url}getUpdates?timeout=1000&offset={update_id + 1}"
        response = requests.get(url)
        return json.loads(response.content)
 
    def create_answer(self, text):
        answer = f"Você disse: {text}"
        return answer

    def send_answer(self, chat_id, answer):
        link_to_send = f"{self.base_url}sendMessage?chat_id={chat_id}&text={answer}"
        requests.get(link_to_send)
        return
