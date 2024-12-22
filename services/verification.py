from services.file_service import load_user_file
from services.user_functions.user_service import check_user_existence
from services.retrieval import get_all_ids
from settings.tokens import *

def is_username_free(username) :
    ids = get_all_ids(USERS)
    for ID in ids :
        user_data = load_user_file(ID)
        if user_data[USERNAME] == username :
            return False
    return True

def get_id_from_username(username) :
    ids = get_all_ids(USERS, include_zero = True)
    for ID in ids :
        user_data = load_user_file(ID)
        if user_data[USERNAME] == username :
            return ID
    return None
    

def verify_user(username, password) :
    user_id = get_id_from_username(username)
    
    if not check_user_existence(user_id) : return False
    
    user_data = load_user_file(user_id)
    
    if user_data[PASSWORD] != password :
        print("Wrong password")
        return False
    return True

def is_admin(user_id) :
    return load_user_file(user_id)[ADMIN]

def is_visible(user_id) :
    return load_user_file(user_id)[VISIBLE]