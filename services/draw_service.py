from services.file_service import load_settings
from services.user_functions.user_draw import get_all_choosable, get_all_choosers, generate_valid_assignment
from services.user_functions.user_service import assign, check_user_existence
from services.file_service import load_user_data, load_item_data, save_user_data, save_item_data
from services.item_functions.item_service import delete_item
from settings.tokens import *
from services.lists_service import get_all_users

def main_draw(user_id) :
    
    settings = load_settings()
    if not settings[LOTTERY_ACTIVE] :
        print("Cannot assign another user due to lottery being inactive")
        return None
    
    if not check_user_existence(user_id) :
        return None
    
    user_data = load_user_data(user_id)
    
    if not user_data[CHOOSABLE] :
        print("User", user_id, "does not participate in lottery")
        return None
    
    choosers = get_all_choosers()
    choosable = get_all_choosable()
    

    redrawal = user_data[ASSIGNMENT] is not None

    if redrawal :
        prev_assignment_ID = user_data[ASSIGNMENT]
        choosers.append(user_id)
        choosable.append(prev_assignment_ID)
    
    choosable.sort()
    
    assignment = generate_valid_assignment(choosers, choosable)
    if assignment is None : return None
    user_index = None
    for i in range(len(choosers)) :
        if choosers[i] == user_id :
            user_index = i
            break
    new_assignment_ID = assignment[user_index]
    assign(user_id, new_assignment_ID)
    return new_assignment_ID

def reset_draw() :
    for user in get_all_users().values() :
        for item_id in user[RESERVED_ITEMS] :
            item_data = load_item_data(item_id)
            if item_data[BOUGHT] :
                item_data[BOUGHT] = False
                save_item_data(item_data)
                delete_item(item_id)
        user = load_user_data(user[USER_ID])
        user[ASSIGNMENT] = None
        user[ASSIGNED_TO] = None
        save_user_data(user)