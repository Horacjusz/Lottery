from services.file_service import load_user_file, save_user_file, save_item_file, load_item_file, delete_item_file
from services.user_functions.user_service import check_user_existence
from settings.tokens import *
from settings.settings import DEFAULT_ITEM_NAME
from services.retrieval import get_free_id
from services.database import datasession
from models.models import Item

def check_item_existence(item_id):
    item = datasession.query(Item).filter_by(item_id=item_id).first()
    if not item:
        print(f"Item with ID {item_id} does not exist.")
        return False
    return True


def create_item(owner_id, item_data = None) :
    if item_data is None :
        item_data = {}
    if item_data.get(ITEM_ID) is None :
        item_data[ITEM_ID] = get_free_id(ITEMS)
    if item_data.get(ITEM_NAME) is None :
        item_data[ITEM_NAME] = DEFAULT_ITEM_NAME
    if item_data.get(ITEM_DESCRIPTION) is None :
        item_data[ITEM_DESCRIPTION] = ""
    if item_data.get(RESERVED_BY) is None :
        item_data[RESERVED_BY] = None
    if item_data.get(OWNER_ID) is None :
        item_data[OWNER_ID] = owner_id
    if item_data.get(BOUGHT) is None :
        item_data[BOUGHT] = False
    item_id = item_data[ITEM_ID]
    save_item_file(item_data)
    add_item_to_wishlist(owner_id, item_id)
    print(f"Item {item_id} created and saved")
    return item_data

def add_item_to_wishlist(user_id, item_id) :
    if not check_user_existence(user_id) :
        return False
    if not check_item_existence(item_id) :
        return False
    user_data = load_user_file(user_id)
    user_data[WISHLIST].append(item_id)
    save_user_file(user_data)
    print(f"Item {item_id} has been added to user {user_id}'s wishlist")
    
def delete_item(item_id) :
    if not check_item_existence(item_id) :
        return True
    item_data = load_item_file(item_id)
    user_data = load_user_file(item_data[OWNER_ID])
    user_data[WISHLIST].remove(item_id)
    save_user_file(user_data)
    unreserve_item(item_id)
    delete_item_file(item_id)
    return True

def edit_item(item_id, new_name=None, new_description=None) :
    if not check_item_existence(item_id) :
        return False
    item_data = load_item_file(item_id)
    if new_name is not None :
        item_data[ITEM_NAME] = new_name
    if new_description is not None :
        item_data[ITEM_DESCRIPTION] = new_description
    save_item_file(item_data)
    print(f"Item {item_id} has been edited")
    return item_data

def reserve_item(user_id, item_id) :
    if not check_user_existence(user_id) :
        return False
    if not check_item_existence(item_id) :
        return False
    user_data = load_user_file(user_id)
    if item_id in user_data[WISHLIST] :
        print("Cannot reserve your own item")
        return False
    user_data[RESERVED_ITEMS].append(item_id)
    save_user_file(user_data)
    item_data = load_item_file(item_id)
    item_data[RESERVED_BY] = user_id
    save_item_file(item_data)
    print(f"Item {item_id} has been reserved by user {user_id}")
    return item_data

def unreserve_item(item_id) :
    print("unreserving", item_id)
    if not check_item_existence(item_id) :
        print(f"Item {item_id} does not exist")
        return False
    item_data = load_item_file(item_id)
    print(item_data)
    if item_data[BOUGHT] :
        print("Cannot unreserve item, because it was already bought")
        return False
    user_id = item_data[RESERVED_BY]
    item_data[RESERVED_BY] = None
    save_item_file(item_data)
    if user_id is None : 
        print(f"Item {item_id} has been unreserved")
        return item_data
    user_data = load_user_file(user_id)
    user_data[RESERVED_ITEMS].remove(item_id)
    save_user_file(user_data)
    print(f"Item {item_id} has been unreserved")
    return item_data

def toggle_buy_item(item_id) :
    check_item_existence(item_id)
    item_data = load_item_file(item_id)
    item_data[BOUGHT] = not item_data[BOUGHT]
    save_item_file(item_data)
    print(f"Item {item_id} bought? {item_data[BOUGHT]}")
    return item_data[BOUGHT]