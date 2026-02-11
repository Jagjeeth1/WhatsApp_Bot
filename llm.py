import requests
import json


def ask_llama(message: str):

    prompt = f"""
You are a strict JSON classification engine.

You MUST reply with ONLY valid JSON.
No explanations.
No extra text.
No sentences.

Return EXACTLY this format:

{{
  "is_task": true or false,
  "needs_clarification": true or false
}}

Rules:
A task NEEDS clarification if it lacks ANY of these:

- What exactly should be done
- A clear description of the work
- Enough detail for someone to execute it without asking questions

Examples that NEED clarification:
- "do this work"
- "handle it"
- "take care of the task"
- "finish this"
- "look into it"

Examples that DO NOT need clarification:
- "fix the login bug"
- "deploy backend at 5pm"
- "update pricing page"

Classify this message:

{message}
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3:8b",

                "format": "json",

                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0,
                    "top_p": 0
                }
            },
            timeout=30
        )

        raw_output = response.json()["response"]

        print("RAW LLM OUTPUT:", raw_output)

        result = json.loads(raw_output)

        return {
            "is_task": bool(result.get("is_task", False)),
            "needs_clarification": bool(result.get("needs_clarification", False))
        }

    except Exception as e:
        print("Llama error:", e)

        return {"is_task": False, "needs_clarification": False}
