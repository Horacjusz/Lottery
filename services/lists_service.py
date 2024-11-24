from settings.tokens import *
from services.retrieval import get_all_ids
from services.file_service import load_user_data, load_item_data

def get_available_spouses() :
    ids = get_all_ids(USERS)
    spouses = []
    for ID in ids :
        spouse = load_user_data(ID)
        if spouse[SPOUSE] is None :
            spouses.append(spouse)
    return spouses

def get_all_users() :
    ids = get_all_ids(USERS)
    users = {}
    for ID in ids :
        users[ID] = (load_user_data(ID))
    return users

def get_all_items() :
    ids = get_all_ids(ITEMS)
    items = {}
    for ID in ids :
        items[ID] = (load_item_data(ID))
    return items