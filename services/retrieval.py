import os
from settings.settings import USERS_PATH, ITEMS_PATH
from settings.tokens import *

def get_all_ids(kind, include_zero = False):
    ids = []
    path = USERS_PATH if kind == USERS else ITEMS_PATH if kind == ITEMS else None
    try:
        for filename in os.listdir(path):
            if (filename.startswith("user_") or filename.startswith("item_")) and filename.endswith(".json"):
                this_id = filename[5:-5]
                if this_id.isdigit():
                    if int(this_id) == 0 and include_zero == False : continue
                    ids.append(int(this_id))
    except FileNotFoundError:
        print(f"Directory {USERS_PATH} does not exist.")
    return sorted(ids)

def get_free_id(kind) :
    ids = get_all_ids(kind)
    if len(ids) == 0 : return 1
    for i in range(1, len(ids)) :
        if ids[i] - ids[i - 1] > 1 :
            return ids[i - 1] + 1
    return ids[-1] + 1

def user_file_path(user_id) :
    return os.path.join(USERS_PATH, f"user_{user_id}.json")

def item_file_path(item_id) :
    return os.path.join(ITEMS_PATH, f"item_{item_id}.json")

# def test_user_retrieval():
#     print("Testing user_retrieval...")
#     user_ids = get_all_user_ids()
#     print("Retrieved User IDs:", user_ids)
#     first_free_id = get_free_id()
#     print("First free ID is:", first_free_id)
