import requests
from config import GRAPH_BASE_URL


def get_display_name(token):
    graph_url = f"{GRAPH_BASE_URL}/me?$select=displayName"

    headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
    }

    response = requests.get(graph_url, headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        display_name = user_data.get("displayName")
        return display_name
    else:
        raise RuntimeError(response.status_code, response.text)