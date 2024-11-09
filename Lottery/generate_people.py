import json
import os
import random
from faker import Faker
from cipher_data import encrypt_file, decrypt_file
from data_create import data_initialize, add_person

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(SCRIPT_PATH, "data")  # Ścieżka do katalogu `data`
fake = Faker()
MAX_RANDOM_PERSONS = 10  # Liczba losowych osób do wygenerowania
MARRIAGE_PERCENTAGE = 0.8  # Procent osób będących w związku małżeńskim

def generate_random_person(person_id):
    """
    Funkcja generująca losowe dane osoby.
    """
    return {
        "id": person_id,
        "name": fake.name(),
        "spouse": None,  # Początkowo brak małżonka
        "wishlist": [fake.word() for _ in range(3)]  # Lista losowych prezentów
    }

def assign_marriages(persons):
    """
    Przypisuje małżonków do około 80% losowych osób z listy.
    """
    num_married = int(len(persons) * MARRIAGE_PERCENTAGE) // 2 * 2  # Zaokrąglenie do parzystej liczby
    random.shuffle(persons)  # Losowe przemieszanie listy osób

    for i in range(0, num_married, 2):
        # Przypisanie osoby (i) do małżonka (i+1) i odwrotnie
        persons[i]["spouse"] = persons[i + 1]["name"]
        persons[i + 1]["spouse"] = persons[i]["name"]

if __name__ == "__main__":
    # Inicjalizacja plików z pustymi słownikami
    data_initialize()

    # Tworzenie losowych osób i dodawanie ich do listy
    persons = [generate_random_person(str(i)) for i in range(1, MAX_RANDOM_PERSONS + 1)]

    # Przypisanie małżeństw
    assign_marriages(persons)

    # Dodawanie osób do zaszyfrowanych plików
    for person_data in persons:
        add_person(person_data)
        print(f"Dodano losową osobę: {person_data['name']}, Małżonek: {person_data['spouse']}")
