from config import CACHE_FILE, CLIENT_ID, SCOPES
import os
from msal import PublicClientApplication, SerializableTokenCache


def get_access_token():
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
    if "access_token" not in result:
        raise RuntimeError(f"Authentication failed: {result.get('error_description')}")
    if cache.has_state_changed:
        with open(CACHE_FILE, "w") as f:
            f.write(cache.serialize())
            
    return result["access_token"]