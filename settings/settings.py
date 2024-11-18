import os
import json

# Get the absolute path to the project directory
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_PATH = os.path.join(PROJECT_PATH, "data")
os.makedirs(DATA_PATH, exist_ok=True)
CONFIG_PATH = os.path.join(DATA_PATH, "config.json")
USERS_PATH = os.path.join(PROJECT_PATH, "data", "users")
os.makedirs(USERS_PATH, exist_ok=True)
ITEMS_PATH = os.path.join(PROJECT_PATH, "data", "items")
os.makedirs(ITEMS_PATH, exist_ok=True)
USERNAMES_PATH = os.path.join(PROJECT_PATH, "data", "users", "usernames.json")
os.makedirs(USERS_PATH, exist_ok=True)
DEFAULT_PASSWORD = "test"


# Default settings
DEFAULT_SETTINGS = {
    "LOTTERY_ACTIVE": False
}

# Ensure config.json exists
if not os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "w") as file:
        json.dump(DEFAULT_SETTINGS, file, indent=4)
        
# Ensure usernames.json exists
if not os.path.exists(USERNAMES_PATH):
    with open(USERNAMES_PATH, "w") as file:
        json.dump({}, file, indent=4)

# Load settings from the config.json file
def load_settings():
    try:
        if not os.path.exists(CONFIG_PATH):
            # If config.json does not exist, create it with default settings
            save_settings(DEFAULT_SETTINGS)
        with open(CONFIG_PATH, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading settings: {e}, returning DEFAULT_SETTINGS")
        return DEFAULT_SETTINGS

# Save settings to the config.json file
def save_settings(data):
    if not isinstance(data, dict):
        raise ValueError("Data must be a dictionary.")
    with open(CONFIG_PATH, 'w') as file:
        json.dump(data, file, indent=4)

def test_settings() :
    # Test the settings module
    print("Project Path:", PROJECT_PATH)

    # Load settings
    settings = load_settings()
    print("Loaded Settings:", settings)

    # Save new settings
    new_data = {**settings, "LOTTERY_ACTIVE": True}  # Toggle LOTTERY_ACTIVE
    save_settings(new_data)
    print("Settings saved!")

    # Reload settings
    settings = load_settings()
    print("Reloaded Settings:", settings)

    # Save new settings
    new_data = {**settings, "LOTTERY_ACTIVE": False}  # Toggle LOTTERY_ACTIVE
    save_settings(new_data)
    print("Settings saved!")

    # Reload settings
    settings = load_settings()
    print("Reloaded Settings:", settings)
