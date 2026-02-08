import requests
import os
from dotenv import load_dotenv

load_dotenv()

LINEAR_API_KEY = os.getenv("LINEAR_API_KEY")
TEAM_ID = os.getenv("LINEAR_TEAM_ID")


def create_linear_issue(title):
    """
    Creates a Linear issue using the message text as the title.
    """

    url = "https://api.linear.app/graphql"

    headers = {
        "Authorization": LINEAR_API_KEY,
        "Content-Type": "application/json"
    }

    query = """
    mutation ($title: String!, $teamId: String!) {
      issueCreate(input: { title: $title, teamId: $teamId }) {
        issue {
          id
          title
          url
        }
      }
    }
    """

    variables = {
        "title": title,
        "teamId": TEAM_ID
    }
    print("🔥 TEAM_ID LOADED:", TEAM_ID)

    try:
        response = requests.post(
            url,
            json={"query": query, "variables": variables},
            headers=headers,
            timeout=20
        )

        data = response.json()

        print("Linear issue created:")
        print(data)

        return data

    except Exception as e:
        print("Linear error:", e)
        return None


