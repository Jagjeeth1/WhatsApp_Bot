import requests


def ask_llama(message):

    prompt = f"""
You are a strict classification engine.

Classify the WhatsApp message into ONE label only:

TASK
NOT_TASK

TASK means:
- Work is assigned
- Someone is told to do something
- An action is requested

NOT_TASK means:
- Greetings
- Conversations
- Status updates
- Informational messages

Reply with ONLY ONE WORD.

TASK
or
NOT_TASK

Message:
"{message}"
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3:8b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0,
                    "top_p": 0
                }
            },
            timeout=30
        )

        raw_output = response.json()["response"].strip().upper()

        print(" RAW LLM OUTPUT:", raw_output)

        if raw_output.startswith("TASK"):
            return {"is_task": True}

        return {"is_task": False}

    except Exception as e:
        print("⚠️ Llama error:", e)

        return {"is_task": False}
