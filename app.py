from fastapi import FastAPI, Request
from db import save_message
from llm import ask_llama

app = FastAPI()


@app.get("/")
def home():
    return {"status": "running"}


@app.post("/webhook")
async def webhook(request: Request):

    data = await request.json()

    try:
        message_text = data["messages"][0]["text"]["body"]
    except Exception:
        print("⚠️ Could not extract message from payload:", data)
        return {"status": "ignored"}

    print("\n MESSAGE:", message_text)

    save_message(message_text)
    
    try:
        result = ask_llama(message_text)
        print("AI SAYS:", result)

        if result.get("is_task"):
            print("TASK DETECTED!")

    except Exception as e:
        print("Ollama error:", e)

    return {"status": "ok"}
