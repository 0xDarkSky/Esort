from pathlib import Path
import os
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CACHE_FILE = PROJECT_ROOT / "token_cache.json"
DB_FILE = PROJECT_ROOT / "esort.db"
SCOPES = ["Mail.Read", "User.Read"]
GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"

load_dotenv()
CLIENT_ID = os.environ["APPLICATION_CLIENT_ID"]

