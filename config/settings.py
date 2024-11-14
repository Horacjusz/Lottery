import os

# Base data directory path for encrypted files
SCRIPT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATA_PATH = os.path.join(SCRIPT_PATH, "data")

# File paths for encrypted data
USERS_DATA_FILE = os.path.join(DATA_PATH, "users_data_encrypted")
CHOOSING_FILE = os.path.join(DATA_PATH, "choosing_encrypted")
CHOSEN_FILE = os.path.join(DATA_PATH, "chosen_encrypted")
ASSIGNMENT_FILE = os.path.join(DATA_PATH, "assignment_encrypted")
KEY_PATH = os.path.join(DATA_PATH, "secret.key")

# Default settings
DEFAULT_PASSWORD = "123"  # Default password for randomly generated users

# Percentage of people who will be assigned spouses (e.g., 0.8 for 80%)
MARRIAGE_PERCENTAGE = 0.8

# Number of random persons to generate for initialization
MAX_RANDOM_PERSONS = 10
