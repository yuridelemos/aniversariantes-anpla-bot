import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("API_KEY")
URL_PUBLICA = os.getenv("RENDER_URL")  # ex: https://seu-app.onrender.com
SECRET = os.getenv("WEBHOOK_SECRET")

resposta = requests.post(
    f"https://api.telegram.org/bot{TOKEN}/setWebhook",
    json={
        "url": f"{URL_PUBLICA}/webhook",
        "secret_token": SECRET
    }
)

print(resposta.json())