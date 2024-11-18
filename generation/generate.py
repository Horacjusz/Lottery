from settings.tokens import *
from services.file_service import clear_directory, save_user_file, load_user_file
from settings.settings import USERS_PATH, DEFAULT_PASSWORD, ITEMS_PATH, DATA_PATH, load_settings
from services.user_functions.user_service import create_user, print_user
from services.item_functions.item_service import create_item
from generation.generate_owner import generate_owner
from random import randint
from faker import Faker

faker = Faker()

def main(num_of_users = 10, new_data = True, new_users = True, new_items = True):
    """
    Generate and save 10 random users.
    """
    print("Generating",num_of_users,"random users...")
    if new_data :
        clear_directory(DATA_PATH)
        load_settings()
    else :
        if new_users :
            clear_directory(USERS_PATH)
        if new_items :
            clear_directory(ITEMS_PATH)
    generate_owner()
    for _ in range(num_of_users):
        user = create_user()
        user_id = user[USER_ID]
        save_user_file(user)
        for _ in range(randint(0,5)) :
            create_item(user_id)
        print(f"User {user[USER_ID]} created and saved.")