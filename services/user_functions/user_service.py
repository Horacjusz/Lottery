from services.retrieval import get_free_id, get_all_ids
from services.file_service import save_user_data, load_user_data, delete_user_data
from settings.tokens import *
from settings.settings import DEFAULT_PASSWORD, DEFAULT_NAME
from services.database import datasession
from models.models import User

def check_user_existence(user_id):
    if user_id is None:
        return False
    try:
        user = datasession.query(User).filter_by(user_id=user_id).first()
        if not user:
            print(f"User with ID {user_id} does not exist.")
            return False
        return True
    except Exception as e:
        print(f"Error checking existence of user with ID {user_id}: {e}")
        return False

def create_user(user_data = None) :
    if user_data is None : 
        user_data = {}
    if user_data.get(USER_ID) is None :
        user_data[USER_ID] = get_free_id(USERS)
    if user_data.get(NAME) is None :
        user_data[NAME] = DEFAULT_NAME
    if user_data.get(USERNAME) is None :
        user_data[USERNAME] = f"user_{user_data[USER_ID]}"
    if user_data.get(PASSWORD) is None :
        user_data[PASSWORD] = DEFAULT_PASSWORD
    if user_data.get(VISIBLE) is None :
        user_data[VISIBLE] = True
    if user_data.get(CHOOSABLE) is None :
        user_data[CHOOSABLE] = True
    if user_data.get(SPOUSE) is None :
        user_data[SPOUSE] = None
    if user_data.get(ASSIGNMENT) is None :
        user_data[ASSIGNMENT] = None
    if user_data.get(ASSIGNED_TO) is None :
        user_data[ASSIGNED_TO] = None
    if user_data.get(ADMIN) is None :
        user_data[ADMIN] = False
    if user_data.get(WISHLIST) is None :
        user_data[WISHLIST] = []
    if user_data.get(RESERVED_ITEMS) is None :
        user_data[RESERVED_ITEMS] = []

    if not user_data[VISIBLE] :
        user_data[CHOOSABLE] = False
    
    save_user_data(user_data)
    return user_data

def print_user(user_id) :
    check_user_existence(user_id)
    print(load_user_data(user_id))
    
def print_all_users() :
    for Id in get_all_ids(USERS) :
        print_user(Id)
  
  
def delete_user(user_id):
    
    if not check_user_existence(user_id):
        print("User", user_id, "does not exist.")
        return True

    user_data = load_user_data(user_id)
    
    if not user_data:
        print(f"User {user_id} does not exist in the database.")
        return True

    if user_data[ASSIGNED_TO] is not None and user_data[ASSIGNMENT] is not None :
        from services.draw_service import generate_valid_assignment
        if user_data[ASSIGNED_TO] is not None and user_data[ASSIGNMENT] is None:
            assignment_id = user_data[ASSIGNED_TO]
            edit_user(assignment_id, reset_assignment=True)
            edit_user(user_id, reset_assigned_to=True)
            if generate_valid_assignment() is None:
                edit_user(assignment_id, new_assignment=user_id)
                edit_user(user_id, new_assigned_to=assignment_id)
                print("Cannot delete user due to assignment clutch")
                return False
        elif user_data[ASSIGNMENT] is not None and user_data[ASSIGNED_TO] is None:
            assignment_id = user_data[ASSIGNMENT]
            edit_user(assignment_id, reset_assigned_to=True)
            edit_user(user_id, reset_assignment=True)

            if generate_valid_assignment() is None:
                edit_user(assignment_id, new_assigned_to=user_id)
                edit_user(user_id, new_assignment=assignment_id)
                print("Cannot delete user due to assignment clutch")
                return False
        else :
            from services.user_functions.user_draw import can_be_assigned
            if can_be_assigned(user_data[ASSIGNED_TO], user_data[ASSIGNMENT]):
                assigned_to = user_data[ASSIGNED_TO]
                assignment = user_data[ASSIGNMENT]
                edit_user(assigned_to, new_assignment=assignment)
                edit_user(assignment, new_assigned_to=assigned_to)
            else:
                print("Cannot delete user due to assignment clutch")
                return False
            
    
    from services.item_functions.item_service import delete_item, unreserve_item
    for item_id in user_data[RESERVED_ITEMS] :
        unreserve_item(item_id)


    for item_id in user_data[WISHLIST] :
        delete_item(item_id)

    try:
        datasession.commit()
    except Exception as e:
        datasession.rollback()
        print(f"Failed to delete items for user {user_id}: {e}")
        return False

    return delete_user_data(user_id)

def assign(user_id, assignment_id) :
    user_data = load_user_data(user_id)
    old_assignment = user_data[ASSIGNMENT]
    if old_assignment is not None :
        edit_user(old_assignment, reset_assigned_to = True)
    edit_user(user_id, new_assignment = assignment_id)
    edit_user(assignment_id, new_assigned_to = user_id)
    
def unassign(user_id) :
    user_data = load_user_data(user_id)
    old_assignment = user_data[ASSIGNMENT]
    if old_assignment is not None :
        edit_user(old_assignment, reset_assigned_to = True)
    edit_user(user_id, reset_assignment = True)

def edit_user(user_id,
              new_name = None,
              new_username = None,
              new_visible = None,
              new_choosable = None,
              new_spouse = None,
              reset_spouse = False,
              new_assignment = None,
              reset_assignment = False,
              new_assigned_to = None,
              reset_assigned_to = False,
              new_admin = None,
              new_wishlist = None,
              new_reserved_items = None,
              new_password = None
              ) :
    check_user_existence(user_id)
    user_data = load_user_data(user_id)
    if new_name is not None :
        user_data[NAME] = new_name
    if new_username is not None :
        user_data[USERNAME] = new_username
    if new_visible is not None :
        user_data[VISIBLE] = new_visible
    if new_choosable is not None :
        user_data[CHOOSABLE] = new_choosable
    if new_spouse is not None :
        marriage(user_id, new_spouse)
        user_data[SPOUSE] = new_spouse
    if new_assignment is not None :
        user_data[ASSIGNMENT] = new_assignment
    if new_assigned_to is not None :
        user_data[ASSIGNED_TO] = new_assigned_to
    if new_admin is not None :
        user_data[ADMIN] = new_admin
    if new_wishlist is not None :
        user_data[WISHLIST] = new_wishlist
    if new_reserved_items is not None :
        user_data[RESERVED_ITEMS] = new_reserved_items
    if new_password is not None :
        user_data[PASSWORD] = new_password
        
    if reset_spouse : 
        marriage(user_id)
        user_data[SPOUSE] = None
    if reset_assignment : user_data[ASSIGNMENT] = None
    if reset_assigned_to : user_data[ASSIGNED_TO] = None
    
    if not user_data[VISIBLE] :
        user_data[CHOOSABLE] = False
    
    save_user_data(user_data)
    return user_data

def marriage(user_id, spouse_id = None) :
    user_data = load_user_data(user_id)
    prev_spouse = user_data[SPOUSE]
    if prev_spouse == spouse_id : return
    if prev_spouse is not None :
        prev_spouse_data = load_user_data(prev_spouse)
        prev_spouse_data[SPOUSE] = None
        save_user_data(prev_spouse_data)
    if spouse_id is not None :
        spouse_data = load_user_data(spouse_id)
        prev_spouse_spouse_id = spouse_data[SPOUSE]
        spouse_data[SPOUSE] = user_id
        if prev_spouse_spouse_id is not None :
            prev_spouse_spouse_data = load_user_data(prev_spouse_spouse_id)
            prev_spouse_spouse_data[SPOUSE] = None
            save_user_data(prev_spouse_spouse_data)
        save_user_data(spouse_data)
    user_data[SPOUSE] = spouse_id
    save_user_data(user_data)
    return