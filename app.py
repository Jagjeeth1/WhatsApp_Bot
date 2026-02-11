from fastapi import FastAPI, Request
from db import save_message
from llm import ask_llama
from linear import create_linear_issue

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
        print("Could not extract message from payload:", data)
        return {"status": "ignored"}

    print("\nMESSAGE:", message_text)

    save_message(message_text)

    try:
        result = ask_llama(message_text)
        print("AI SAYS:", result)

        if not result.get("is_task"):
            print("Not a task. Ignoring.")
            return {"status": "not_a_task"}

        
        if result.get("needs_clarification"):
            print("Task detected but needs clarification.")

            return {"status": "needs_clarification"}

        print("Clear task detected — Creating Linear ticket...")
        create_linear_issue(message_text)

    except Exception as e:
        print("Ollama error:", e)

    return {"status": "ok"}
