import json
import os
from cipher_data import encrypt_file, decrypt_file

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(SCRIPT_PATH, "data")

def data_initialize():
    """
    Funkcja inicjalizująca cztery zaszyfrowane puste pliki słowników:
    family_data, chosen_data, choosing_data i assignment.
    """
    # Tworzenie pustych słowników
    family_data = {}
    chosen_data = {}
    choosing_data = {}
    assignment = {}

    # Serializacja i zaszyfrowanie każdego słownika
    encrypt_file(json.dumps(family_data), os.path.join(DATA_PATH, "family_data_encrypted"))
    encrypt_file(json.dumps(chosen_data), os.path.join(DATA_PATH, "chosen_encrypted"))
    encrypt_file(json.dumps(choosing_data), os.path.join(DATA_PATH, "choosing_encrypted"))
    encrypt_file(json.dumps(assignment), os.path.join(DATA_PATH, "assignment_encrypted"))
    
    print("Zaszyfrowane pliki family_data_encrypted, chosen_encrypted, choosing_encrypted i assignment_encrypted zostały utworzone.")

def add_person(person_data):
    family_data = decrypt_file(os.path.join(DATA_PATH, "family_data_encrypted"))
    
    # Generate a new unique ID for each person
    new_id = max([int(key) for key in family_data.keys()], default=0) + 1
    
    # Add the new person data with the generated ID
    family_data[new_id] = {
        "id": new_id,
        "choosable": person_data["choosable"],
        "name": person_data["name"],
        "username": person_data["username"],
        "password": person_data["password"],
        "spouse": person_data.get("spouse"),
        "wishlist": [{"name": item["name"], "description": item["description"]} for item in person_data.get("wishlist", [])],
        "reserved_items": [],
        "assignment" : None
    }

    # Update choosing and chosen files if person is choosable
    if person_data["choosable"]:
        choosing_data = decrypt_file(os.path.join(DATA_PATH, "choosing_encrypted"))
        chosen_data = decrypt_file(os.path.join(DATA_PATH, "chosen_encrypted"))
        
        # Add the person to both choosing and chosen pools
        choosing_data[new_id] = family_data[new_id]
        chosen_data[new_id] = family_data[new_id]
        
        # Encrypt and save updated choosing and chosen data
        encrypt_file(json.dumps(choosing_data, ensure_ascii=False, indent=4), os.path.join(DATA_PATH, "choosing_encrypted"))
        encrypt_file(json.dumps(chosen_data, ensure_ascii=False, indent=4), os.path.join(DATA_PATH, "chosen_encrypted"))

    # Encrypt and save updated family data
    encrypted_data = json.dumps(family_data, ensure_ascii=False, indent=4)
    encrypt_file(encrypted_data, os.path.join(DATA_PATH, "family_data_encrypted"))

    print(f"Added person with ID {new_id}: {person_data['name']}")

