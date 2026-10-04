from config import CACHE_FILE, CLIENT_ID, SCOPES
import os
import requests
from msal import PublicClientApplication, SerializableTokenCache

cache = SerializableTokenCache()
if os.path.exists(CACHE_FILE):
    cache.deserialize(open(CACHE_FILE).read())

app = PublicClientApplication(
    CLIENT_ID,
    token_cache=cache,
    authority="https://login.microsoftonline.com/common")

result = None 

accounts = app.get_accounts()
if accounts:
    chosen = accounts[0]
    result = app.acquire_token_silent(SCOPES, account=chosen)

if not result or "access_token" not in result:
    result = app.acquire_token_interactive(scopes=SCOPES)
if "access_token" in result:
    access_token = result["access_token"]
    if cache.has_state_changed:
        open(CACHE_FILE, "w").write(cache.serialize())

    graph_url = "https://graph.microsoft.com/v1.0/me?$select=displayName"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }

    response = requests.get(graph_url, headers=headers)
    
    if response.status_code == 200:
        user_data = response.json()
        display_name = user_data.get("displayName")
        print(f"User Display Name: {display_name}")
    else:
        print(f"Graph API Error: {response.status_code} - {response.text}")
else:
    print(f"Authentication Failed: {result.get('error_description')}") 
