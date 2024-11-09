import os
import random
import json
from cipher_data import decrypt_file, encrypt_file
from copy import deepcopy

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(SCRIPT_PATH, "data")  # Nowa ścieżka do katalogu `data`

# Główna funkcja losująca z przypisaniem
def main_draw(person_id, family_data_path, pool_files_paths, assignment_path):
    # Wczytanie zaszyfrowanych danych rodziny, puli i przypisań
    family_data = decrypt_file(family_data_path)
    choosing_data = decrypt_file(pool_files_paths[0])
    chosen_data = decrypt_file(pool_files_paths[1])
    assignment = decrypt_file(assignment_path)

    # Sprawdzenie, czy osoba losująca istnieje
    person = family_data.get(person_id)
    if not person:
        print(f"Osoba o ID {person_id} nie istnieje w danych.")
        return None

    print(f"Osoba losująca: {person['name']}")

    # Tworzymy przypisanie losowań dla każdej osoby
    current_assignment = generate_valid_assignment(family_data, choosing_data, chosen_data)

    # Sprawdzamy przypisanie dla wybranej osoby
    drawn_id = current_assignment.get(person_id)
    if drawn_id is None:
        print(f"Dla osoby {person['name']} nie ma dostępnych osób do wylosowania.")
        return None

    # Zapisujemy zmiany po losowaniu
    drawn_person = chosen_data.pop(drawn_id)  # Usunięcie z `pool_data`
    choosing_person = choosing_data.pop(person_id)  # Usunięcie z `pool_data`
    assignment[person_id] = drawn_id  # Aktualizacja przypisania

    # Zapisanie zaktualizowanych danych do plików
    encrypt_file(json.dumps(chosen_data, ensure_ascii=False, indent=4), pool_files_paths[1])
    encrypt_file(json.dumps(choosing_data, ensure_ascii=False, indent=4), pool_files_paths[0])
    encrypt_file(json.dumps(assignment, ensure_ascii=False, indent=4), assignment_path)

    print(f"{choosing_person} wylosował/a: {drawn_person}")
    return drawn_person

def generate_valid_assignment(family_data, choosing_data, chosen_data):
    """
    Funkcja generuje poprawne przypisanie losowania, upewniając się, że każda osoba
    losuje inną osobę, a nie swojego małżonka ani siebie.
    """
    
    valid = False
    people = list(choosing_data.keys())
    possible_draws = list(chosen_data.keys())
    assignment = deepcopy(possible_draws)
    
    while not valid:
        random.shuffle(assignment)
        this_valid = True
        
        for person_number in range(len(people)):
            person_id = people[person_number]
            assigned_person_id = assignment[person_number]
            identity_test = person_id == assigned_person_id
            spouse_test = family_data[str(person_id)]['spouse'] == family_data[str(assigned_person_id)]['name']
            
            if identity_test or spouse_test:
                this_valid = False
                break
            
        valid = this_valid
    
    output = {}
    for i in range(len(assignment)):
        output[people[i]] = assignment[i]
    
    return output

family_data_path = os.path.join(DATA_PATH, "family_data_encrypted")
pool_files_paths = [
    os.path.join(DATA_PATH, "choosing_encrypted"),
    os.path.join(DATA_PATH, "chosen_encrypted")
]
assignment_path = os.path.join(DATA_PATH, "assignment_encrypted")

# Przykład wywołania losowania
main_draw("1", family_data_path, pool_files_paths, assignment_path)
print()
# Przykład wielokrotnego wywołania losowania
for i in range(10):
    main_draw(str(i), family_data_path, pool_files_paths, assignment_path)
    print()
