from services.encryption_service import encrypt_file, decrypt_data
import json
import os
from config.settings import DATA_PATH, MAX_RANDOM_PERSONS
from services.user_service import generate_random_person, assign_marriages, add_person


def data_initialize():
    """
    Funkcja inicjalizująca cztery zaszyfrowane puste pliki słowników:
    family_data, chosen_data, choosing_data i assignment.
    """
    # Tworzenie pustych słowników
    users_data = {}

    # Serializacja i zaszyfrowanie każdego słownika
    encrypt_file(json.dumps(users_data), os.path.join(DATA_PATH, "users_data_encrypted"))
    
    print("Zaszyfrowano plik users_data_encrypted")
    
    
def main(new_data = False):
    if new_data :
        data_initialize()
    from services.encryption_service import decrypt_data
    initial_data = decrypt_data()
    # Tworzenie losowych osób i dodawanie ich do listy
    persons = [generate_random_person(i) for i in range(len(initial_data), MAX_RANDOM_PERSONS + len(initial_data))]

    del initial_data
    # Przypisanie małżeństw
    assign_marriages(persons)

    # Dodawanie osób do zaszyfrowanych plików
    for person_data in persons:
        add_person(person_data)
        # print(person_data)
        print(f"Dodano losową osobę: {person_data.name}, Małżonek: {person_data.spouse}")
        
def data_to_dict(data) :
    return {user_id: user.to_dict() for user_id, user in data.items()}
        
def print_data(person_id) :
    data = decrypt_data()
    print(data[person_id])
        
        
if __name__ == "__main__":
    main()