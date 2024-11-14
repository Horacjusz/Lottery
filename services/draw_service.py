import json
import random
from copy import deepcopy
from services.encryption_service import decrypt_data, encrypt_file
from config.settings import USERS_DATA_FILE


# Główna funkcja losująca z przypisaniem
def main_draw(person_id):
    person_id = str(person_id)
    # Wczytanie zaszyfrowanych danych rodziny, puli i przypisań
    users_data = decrypt_data()

    # print(users_data)
    # print(person_id)
    
    # Sprawdzenie, czy osoba losująca istnieje
    person = users_data.get(person_id)
    if not person:
        print(f"Osoba o ID {person_id} nie istnieje w danych.")
        return None

    # print(f"Osoba losująca: {person.name}")

    # Tworzymy przypisanie losowań dla każdej osoby
    valid_assignment = generate_valid_assignment(users_data, person_id)

    # Sprawdzamy przypisanie dla wybranej osoby
    drawn_id = valid_assignment.get(person_id)
    if drawn_id is None:
        print(f"Dla osoby {person.name} nie ma dostępnych osób do wylosowania.")
        return None
    users_data[person_id].assignment = drawn_id
    # print(users_data[person_id])
    # print(f"{users_data[person_id].name}(spouse {users_data[str(users_data[person_id].spouse)].name}) wylosował/a: {users_data[drawn_id].name}")
    # print(drawn_id)
    return drawn_id



def generate_valid_assignment(users_data, person_id):
    possible_draws = []
    people = []
    # print(users_data)
    for person_ID in users_data :
        person = users_data[person_ID]
        if not person.choosable : continue
        if person.assignment is None :
            people.append(person_ID)
        possible_draws.append(person_ID)
        
    for person_ID in users_data :
        person = users_data[person_ID]
        if not person.choosable : continue
        if person.assignment is not None :
            possible_draws.remove(person.assignment)
    
    # print(people)
    # print(possible_draws)    
                
        
    # print(users_data[person_id])
    # people = [person_id for person_id in choosing_data if users_data[person_id]["choosable"]]
    # possible_draws = [person_id for person_id in chosen_data if users_data[person_id]["choosable"]]
    
    assignment = deepcopy(possible_draws)
    valid = False

    while not valid:
        random.shuffle(assignment)
        this_valid = True

        for person_number in range(len(people)):
            person_id = people[person_number]
            assigned_person_id = assignment[person_number]
            identity_test = person_id == assigned_person_id
            spouse_test = users_data[person_id].spouse == users_data[assigned_person_id].ID

            if identity_test or spouse_test:
                this_valid = False
                break

        valid = this_valid
    # print("people",people)
    # print("assignment",assignment)
    output = {people[i]: assignment[i] for i in range(len(assignment))}
    # print(output)
    return output