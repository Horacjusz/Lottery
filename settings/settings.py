import os
import json
from dotenv import load_dotenv
import os

# Get the absolute path to the project directory
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_PATH = os.path.join(PROJECT_PATH, "data")
os.makedirs(DATA_PATH, exist_ok=True)
CONFIG_PATH = os.path.join(DATA_PATH, "config.json")
USERS_PATH = os.path.join(PROJECT_PATH, "data", "users")
os.makedirs(USERS_PATH, exist_ok=True)
ITEMS_PATH = os.path.join(PROJECT_PATH, "data", "items")
os.makedirs(ITEMS_PATH, exist_ok=True)
DEFAULT_PASSWORD = "test"


# Default settings
DEFAULT_SETTINGS = {
    "LOTTERY_ACTIVE": False
}

# Ensure config.json exists
if not os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "w") as file:
        json.dump(DEFAULT_SETTINGS, file, indent=4)
        

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")