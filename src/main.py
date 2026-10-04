from auth import get_access_token
import requests


try:
    token = get_access_token()
except RuntimeError as e:
    print(e)
    raise SystemExit(1)

graph_url = "https://graph.microsoft.com/v1.0/me?$select=displayName"

headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
}

response = requests.get(graph_url, headers=headers)
    
if response.status_code == 200:
    user_data = response.json()
    display_name = user_data.get("displayName")
    print(f"User Display Name: {display_name}")
else:
    print(f"Graph API Error: {response.status_code} - {response.text}")