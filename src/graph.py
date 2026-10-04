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


def list_messages(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    graph_url = f"{GRAPH_BASE_URL}/me/mailFolders/inbox/messages"

    params = {
        "$select": "id,subject,from,receivedDateTime,isRead",
        "$orderby": "receivedDateTime desc",
        "$top": 20,
    }

    messages = []

    while graph_url:
        try:
            response = requests.get(
                graph_url,
                headers=headers,
                params=params,
                timeout=30
            )

            response.raise_for_status()
            data = response.json()

            messages.extend(data.get("value", []))

            graph_url = data.get("@odata.nextLink")
            params = None

        except requests.exceptions.Timeout:
            raise RuntimeError("Microsoft Graph request timed out")

        except requests.exceptions.ConnectionError:
            raise RuntimeError("Could not connect to Microsoft Graph")

        except requests.exceptions.HTTPError as e:
            status = e.response.status_code

            if status == 401:
                raise RuntimeError(
                    "Access token is invalid or expired"
                ) from e

            elif status == 403:
                raise RuntimeError(
                    "Insufficient permissions. Make sure Mail.Read is granted."
                ) from e

            elif status == 429:
                raise RuntimeError(
                    "Microsoft Graph rate limit exceeded"
                ) from e

            elif status >= 500:
                raise RuntimeError(
                    f"Microsoft Graph server error: HTTP {status}"
                ) from e

            else:
                raise RuntimeError(
                    f"Microsoft Graph request failed: HTTP {status}"
                ) from e

        except ValueError as e:
            raise RuntimeError(
                "Microsoft Graph returned invalid JSON"
            ) from e

    return messages
