import requests
import os
from dotenv import load_dotenv

load_dotenv()

WHAPI_TOKEN = os.getenv("WHAPI_TOKEN")

URL = "https://gate.whapi.cloud/messages/text"


def send_whatsapp_message(chat_id, message):

    headers = {
        "Authorization": f"Bearer {WHAPI_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "to": chat_id,
        "body": message
    }

    try:
        response = requests.post(URL, json=payload, headers=headers)
        print("WhatsApp message sent:", response.json())

    except Exception as e:
        print("WhatsApp send error:", e)