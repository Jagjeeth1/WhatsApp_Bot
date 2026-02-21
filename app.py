from fastapi import FastAPI, Request
from db import save_message
from llm import ask_llama
from linear import create_linear_issue
from whatsapp import send_whatsapp_message

app = FastAPI()


@app.get("/")
def home():
    return {"status": "running"}


@app.post("/webhook")
async def webhook(request: Request):

    data = await request.json()

    try:
        if data["messages"][0].get("from_me"):
            return {"status": "bot_message_ignored"}
    except Exception:
        pass

    try:
        message_text = data["messages"][0]["text"]["body"]
        chat_id = data["messages"][0]["chat_id"]
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

            send_whatsapp_message(
                chat_id,
                "I detected a task but it is too vague.\n\n"
                "Please provide:\n"
                "• What exactly needs to be done\n"
                "• Who should do it\n"
                "• Deadline (optional)\n\n"
                "Example:\n"
                "\"Jagjeeth fix the login bug by today\""
            )

            return {"status": "clarification_requested"}

    
        print("Clear task detected — Creating Linear ticket...")
        create_linear_issue(message_text)

    except Exception as e:
        print("Error:", e)

    return {"status": "ok"}