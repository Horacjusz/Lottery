from models.models import User, Item, Setting
from services.database import datasession
from settings.tokens import *


def get_user_database(user_id) :
    try :
        user = datasession.query(User).filter_by(user_id=user_id).first()
        if user : return user
    except Exception as e :
        print(f"User with ID {user_id} not found in the database.\n->{e}")
    return None

def get_item_database(item_id) :
    try :
        item = datasession.query(Item).filter_by(item_id=item_id).first()
        if item:
            return item
    except Exception as e :
        print(f"Item with ID {item_id} not found in the database.\n->{e}")
    return None


def save_user_data(user_data):
    user = get_user_database(user_data[USER_ID])
    if not user:
        user = User(user_id=user_data[USER_ID])
    user.name = user_data.get("name")
    user.username = user_data.get("username")
    user.password = user_data.get("password")
    user.visible = user_data.get("visible", True)
    user.choosable = user_data.get("choosable", True)
    user.spouse = user_data.get("spouse")
    user.assignment = user_data.get("assignment")
    user.assigned_to = user_data.get("assigned_to")
    user.admin = user_data.get("admin", False)
    user.wishlist = user_data.get("wishlist", [])
    user.reserved_items = user_data.get("reserved_items", [])
    datasession.add(user)
    datasession.commit()

def check_user_value(value) :
    data = load_user_as_dict(value)
    if data is None : return None
    return data[USER_ID]

def load_user_data(user_id) :
    user_data = load_user_as_dict(user_id)
    if user_data is None : return None
    for item_id in user_data[WISHLIST] :
        item_data = load_item_data(item_id)
        if item_data is None :
            print(f"Item with ID {item_id} not found in the database.")
            user_data[WISHLIST].remove(item_id)
    for item_id in user_data[RESERVED_ITEMS] :
        item_data = load_item_data(item_id)
        if item_data is None :
            print(f"Item with ID {item_id} not found in the database.")
            user_data[RESERVED_ITEMS].remove(item_id)
            
    user_data[ASSIGNMENT] = check_user_value(user_data[ASSIGNMENT])
    user_data[ASSIGNED_TO] = check_user_value(user_data[ASSIGNED_TO])
    user_data[SPOUSE] = check_user_value(user_data[SPOUSE])
            
    save_user_data(user_data)
    return user_data

def load_item_data(item_id) :
    item_data = load_item_as_dict(item_id)
    if item_data is None : return None
    if not isinstance(item_data[OWNER_ID], int) :
        print(f"Invalid OWNER_ID: {item_data[OWNER_ID]} (must be an integer).")
        delete_item_data(item_id)
        return None
    owner_exists = get_user_database(item_data[OWNER_ID])
    if not owner_exists :
        print(f"User with ID {item_data[OWNER_ID]} (OWNER_ID) not found in the database.")
        delete_item_data(item_id)
        return None
    if item_data[RESERVED_BY] is not None :
        if not isinstance(item_data[RESERVED_BY], int) :
            print(f"Invalid RESERVED_BY: {item_data[RESERVED_BY]} (must be an integer or None).")
            item_data[RESERVED_BY] = None
        reserved_by_exists = get_user_database(item_data[RESERVED_BY])
        if not reserved_by_exists :
            print(f"User with ID {item_data[RESERVED_BY]} (RESERVED_BY) not found in the database.")
            item_data[RESERVED_BY] = None
    save_item_data(item_data)
    return item_data

def load_user_as_dict(user_id) :
    user = get_user_database(user_id)
    if user :
        user_dict = {
            USER_ID: user.user_id,
            NAME: user.name,
            USERNAME: user.username,
            PASSWORD: user.password,
            VISIBLE: user.visible,
            CHOOSABLE: user.choosable,
            SPOUSE: user.spouse,
            ASSIGNMENT: user.assignment,
            ASSIGNED_TO: user.assigned_to,
            ADMIN: user.admin,
            WISHLIST: user.wishlist,
            RESERVED_ITEMS: user.reserved_items,
        }
        return user_dict
    return None


def load_item_as_dict(item_id) :
    item = get_item_database(item_id)
    if item:
        item_data = {
            ITEM_ID: item.item_id,
            ITEM_NAME: item.item_name,
            ITEM_DESCRIPTION: item.item_description,
            RESERVED_BY: item.reserved_by,
            OWNER_ID: item.owner_id,
            BOUGHT: item.bought,
        }
        return item_data
    return None

def delete_user_data(user_id):
    """
    Delete a user from the database by their ID.
    """
    try:
        user = get_user_database(user_id)
        if user:
            datasession.delete(user)
            datasession.commit()
            print(f"User with ID {user_id} deleted.")
        else:
            print(f"User with ID {user_id} does not exist.")
    except Exception as e:
        print(f"Error deleting user with ID {user_id}: {e}")
    
    
def save_item_data(item_data):
    item = get_item_database(item_data[ITEM_ID])
    if not item:
        item = Item(item_id=item_data[ITEM_ID])
    item.item_name = item_data.get("item_name")
    item.item_description = item_data.get("item_description", "")
    item.reserved_by = item_data.get("reserved_by")
    item.owner_id = item_data.get("owner_id")
    item.bought = item_data.get("bought", False)
    datasession.add(item)
    datasession.commit()


def delete_item_data(item_id):
    """
    Delete an item from the database by its ID.
    """
    try:
        item = get_item_database(item_id)
        if item:
            datasession.delete(item)
            datasession.commit()
            print(f"Item with ID {item_id} deleted.")
        else:
            print(f"Item with ID {item_id} does not exist.")
    except Exception as e:
        print(f"Error deleting item with ID {item_id}: {e}")
    
    
def load_settings():
    """
    Load all settings from the database as a dictionary.
    
    Returns:
        dict: Settings as key-value pairs.
    """
    settings = {}
    try:
        query = datasession.query(Setting).all()
        for setting in query:
            settings[setting.key] = setting.value
    except Exception as e:
        print(f"Error loading settings from database: {e}")
    return settings

def save_settings(data):
    """
    Save settings to the database.
    
    Args:
        data (dict): Settings to save as key-value pairs.
    """
    try:
        for key, value in data.items():
            setting = datasession.query(Setting).filter_by(key=key).first()
            if setting:
                setting.value = value
            else:
                setting = Setting(key=key, value=value)
                datasession.add(setting)
        datasession.commit()
    except Exception as e:
        print(f"Error saving settings to database: {e}")
        

def get_all_ids(kind, include_zero=False):
    ids = []
    try:
        if kind == USERS:
            query = datasession.query(User.user_id)
        elif kind == ITEMS:
            query = datasession.query(Item.item_id)
        else:
            raise ValueError("Invalid kind specified. Must be USERS or ITEMS.")
        
        ids = [row[0] for row in query.all()]
        
        if not include_zero:
            ids = [id for id in ids if id != 0]
    except Exception as e:
        print(f"Error querying IDs from the database: {e}")
    
    return sorted(ids)