import requests
import os
from dotenv import load_dotenv

load_dotenv()

WHAPI_TOKEN = os.getenv("WHAPI_TOKEN")

URL = "https://gate.whapi.cloud/messages/text"


def send_whatsapp_message(to, message):

    headers = {
        "Authorization": f"Bearer {WHAPI_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "to": to,
        "body": message
    }

    try:
        response = requests.post(URL, json=payload, headers=headers)
        print("WhatsApp response:", response.json())

    except Exception as e:
        print("WhatsApp send error:", e)