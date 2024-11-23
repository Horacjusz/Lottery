from models.models import User, Item, Setting
from services.database import datasession
from settings.tokens import *

def save_user_file(user_data):
    user = datasession.query(User).filter_by(user_id=user_data[USER_ID]).first()
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


def load_user_file(user_id):
    user = datasession.query(User).filter_by(user_id=user_id).first()
    if user:
        return {
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
    raise FileNotFoundError(f"User with ID {user_id} not found in the database.")


def delete_user_file(user_id):
    """
    Delete a user from the database by their ID.
    """
    try:
        user = datasession.query(User).filter_by(user_id=user_id).first()
        if user:
            datasession.delete(user)
            datasession.commit()
            print(f"User with ID {user_id} deleted.")
        else:
            print(f"User with ID {user_id} does not exist.")
    except Exception as e:
        print(f"Error deleting user with ID {user_id}: {e}")
    
    
def save_item_file(item_data):
    item = datasession.query(Item).filter_by(item_id=item_data[ITEM_ID]).first()
    if not item:
        item = Item(item_id=item_data[ITEM_ID])
    item.item_name = item_data.get("item_name")
    item.item_description = item_data.get("item_description", "")
    item.reserved_by = item_data.get("reserved_by")
    item.owner_id = item_data.get("owner_id")
    item.bought = item_data.get("bought", False)
    datasession.add(item)
    datasession.commit()


def load_item_file(item_id):
    item = datasession.query(Item).filter_by(item_id=item_id).first()
    if item:
        return {
            ITEM_ID: item.item_id,
            ITEM_NAME: item.item_name,
            ITEM_DESCRIPTION: item.item_description,
            RESERVED_BY: item.reserved_by,
            OWNER_ID: item.owner_id,
            BOUGHT: item.bought,
        }
    raise FileNotFoundError(f"Item with ID {item_id} not found in the database.")


def delete_item_file(item_id):
    """
    Delete an item from the database by its ID.
    """
    try:
        item = datasession.query(Item).filter_by(item_id=item_id).first()
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
        print(query)
        for setting in query:
            print(setting)
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