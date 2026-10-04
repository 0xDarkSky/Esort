from auth import get_access_token
from graph import get_display_name
from graph import list_messages

try:
    token = get_access_token()
    name = get_display_name(token)
    print(name)
except RuntimeError as e:
    print(e)
    raise SystemExit(1)

messages = list_messages(token)
print(messages)