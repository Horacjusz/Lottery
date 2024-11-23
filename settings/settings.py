import os
import json
from dotenv import load_dotenv
import os
from faker import Faker

FAKER = Faker()

# Get the absolute path to the project directory
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DEFAULT_PASSWORD = "test"
DEFAULT_NAME = "Użytkownik"
DEFAULT_ITEM_NAME = "Przedmiot"


# Default settings
DEFAULT_SETTINGS = {
    "LOTTERY_ACTIVE": False
}
        

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")