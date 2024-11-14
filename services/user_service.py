from services.encryption_service import decrypt_file, encrypt_file, decrypt_data, encrypt_data
from config.settings import USERS_DATA_FILE, DEFAULT_PASSWORD, DATA_PATH, MARRIAGE_PERCENTAGE
from services.encryption_service import update_pool_files
from flask import flash
import json
import os
from faker import Faker
import random
from models.user import User

fake = Faker()

def verify_username(username) :
    users_data = decrypt_file(USERS_DATA_FILE)
    # print(users_data)
    for user in users_data.values():
        if user["username"] == username :
            return False
    return True

def verify_user(username, password):
    users_data = decrypt_file(USERS_DATA_FILE)
    # print(users_data)
    for user in users_data.values():
        if user["username"] == username and user["password"] == password:
            return True
    return False

def get_id(username) :
    users_data = decrypt_data()
    for user in users_data.values():
        if user.username == username:
            return user.ID
        
def validate_passwords(password, confirm_password):
    if password != confirm_password:
        flash("Hasła nie są zgodne.", "error")
        return False
    return True

def add_user(user_data):
    
    # print("Adding user")
    
    users_data = decrypt_file(USERS_DATA_FILE)
    
    # Generate a new unique integer ID for each user
    new_id = max([int(key) for key in users_data.keys()], default=0) + 1
    user_data["id"] = new_id
    user_data["reserved_items"] = []  # Initialize reserved items
    user_data["choosable"] = user_data.get("choosable", True)  # Domyślnie True
    user_data["wishlist"] = [
        {"name": item["name"], "description": item["description"], "reserved_by": None} 
        for item in user_data.get("wishlist", [])
    ]
    
    users_data[new_id] = user_data
    # update_pool_files(users_data)

    # Encrypt and save updated data
    encrypted_data = json.dumps(users_data, ensure_ascii=False, indent=4)
    encrypt_file(encrypted_data, USERS_DATA_FILE)
    # Encrypt and save updated data
    encrypted_data = json.dumps(users_data, ensure_ascii=False, indent=4)
    encrypt_file(encrypted_data, USERS_DATA_FILE)
    return True

def get_user_wishlist(user_id):
    """
    Retrieves the wishlist for a user based on their unique ID.
    Only shows items that are either unreserved or reserved by the user themselves.
    """
    users_data = decrypt_file(USERS_DATA_FILE)
    user_data = users_data.get(str(user_id))
    if not user_data:
        return []

    return [
        item for item in user_data.get("wishlist", [])
        if item["reserved_by"] is None or item["reserved_by"] == user_id
    ]
    
def add_to_wishlist(user_id, item_name, item_description):
    users_data = decrypt_file(USERS_DATA_FILE)
    
    # print(user_id)
    
    if str(user_id) not in users_data:
        return False  # User not found
    
    users_data[str(user_id)]["wishlist"].append({
        "name": item_name,
        "description": item_description,
        "reserved_by": None  # Set reserved_by to None initially
    })

    # Encrypt and save updated data
    encrypted_data = json.dumps(users_data, ensure_ascii=False, indent=4)
    encrypt_file(encrypted_data, USERS_DATA_FILE)
    return True

def remove_from_wishlist(user_id, item_name, item_description):
    users_data = decrypt_file(USERS_DATA_FILE)

    if str(user_id) in users_data and "wishlist" in users_data[str(user_id)]:
        
        reservationist = None
        for userID in users_data :
            if userID == str(user_id) :
                for item in users_data[userID]["wishlist"] :
                    if item["name"] == item_name and item["description"] :
                        reservationist = item["reserved_by"]
                        break
                break
        if reservationist is not None :
            users_data[reservationist]["reserved_items"].remove({"name" : item_name, "description" : item_description})
        
        wishlist = users_data[str(user_id)]["wishlist"]
        users_data[str(user_id)]["wishlist"] = [
            item for item in wishlist if not (item["name"] == item_name and item["description"] == item_description)
        ]
        
            

        # Encrypt and save updated data
        encrypted_data = json.dumps(users_data, ensure_ascii=False, indent=4)
        encrypt_file(encrypted_data, USERS_DATA_FILE)
        
        
def get_available_spouses(users_data, exclude=None):
    """
    Returns a list of available spouses (users without a spouse) excluding the specified user by username.
    """
    return [
        {"id": user_id, "name": user.name}
        for user_id, user in users_data.items()
        if user.spouse is None and user.username != exclude
    ]
    
    
def add_person(person):
    users_data = decrypt_data(as_dict = True)
    users_data[person.ID] = person.to_dict()
    
    encrypted_data = json.dumps(users_data, ensure_ascii=False, indent=4)
    encrypt_data(encrypted_data)

    # print(f"Added person with ID {person.ID}: {person.name}")
    
    
    
def generate_random_person(person_id):
    """
    Funkcja generująca losowe dane osoby.
    """
    return User(person_id, fake.name(), f"user_{person_id}", DEFAULT_PASSWORD, True, None, None, [{"name": fake.word(), "description": fake.sentence(), "reserved_by": None} for _ in range(3)], [])
    

def assign_marriages(persons):
    """
    Przypisuje małżonków do około 80% losowych osób z listy.
    """
    num_married = int(len(persons) * MARRIAGE_PERCENTAGE) // 2 * 2
    random.shuffle(persons)

    for i in range(0, num_married, 2):
        persons[i].spouse = persons[i + 1].ID
        persons[i + 1].spouse = persons[i].ID
        
        
if __name__ == ("__main__") :
    print("test")