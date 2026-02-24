import requests
import os
from dotenv import load_dotenv
from whatsapp import send_whatsapp_message

load_dotenv()

LINEAR_API_KEY = os.getenv("LINEAR_API_KEY")
TEAM_ID = os.getenv("LINEAR_TEAM_ID")

URL = "https://api.linear.app/graphql"


def get_pending_issues():
    query = """
    query ($teamId: ID!) {
      issues(
        filter: {
          team: { id: { eq: $teamId } }
          state: { type: { neq: "completed" } }
        }
      ) {
        nodes {
          identifier
          title
          url
        }
      }
    }
    """

    headers = {
        "Authorization": LINEAR_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(
        URL,
        json={"query": query, "variables": {"teamId": TEAM_ID}},
        headers=headers
    )

    data = response.json()
    print("Linear response:", data)

    return data["data"]["issues"]["nodes"]

GROUP_CHAT_ID = "120363408236875852@g.us"


def send_pending_tasks():
    print("Fetching pending issues from Linear...")

    issues = get_pending_issues()

    print("Issues fetched:", issues)

    if not issues:
        message = "No pending Linear tasks. Great job team!"
    else:
        message = "Pending Linear tasks:\n\n"

        for i in issues:
            message += f"{i['identifier']} - {i['title']}\n{i['url']}\n\n"

    print("Sending message to WhatsApp...")

    send_whatsapp_message(GROUP_CHAT_ID, message)