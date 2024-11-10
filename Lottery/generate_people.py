import os
import random
from faker import Faker
from data_create import data_initialize, add_person

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(SCRIPT_PATH, "data")
fake = Faker()
MAX_RANDOM_PERSONS = 10  # Liczba losowych osób do wygenerowania
MARRIAGE_PERCENTAGE = 0.8  # Procent osób będących w związku małżeńskim
DEFAULT_PASSWORD = "123"  # Domyślne hasło dla każdego użytkownika

def generate_random_person(person_id):
    """
    Funkcja generująca losowe dane osoby.
    """
    return {
        "id": person_id,
        "name": fake.name(),
        "username": f"user_{person_id}",
        "password": DEFAULT_PASSWORD,
        "spouse": None,
        # Wishlist jako lista słowników z "name" i "description" dla każdego przedmiotu
        "wishlist": [{"name": fake.word(), "description": fake.sentence()} for _ in range(3)],
        "choosable": True,
        "assignment" : None
    }

def assign_marriages(persons):
    """
    Przypisuje małżonków do około 80% losowych osób z listy.
    """
    num_married = int(len(persons) * MARRIAGE_PERCENTAGE) // 2 * 2
    random.shuffle(persons)

    for i in range(0, num_married, 2):
        persons[i]["spouse"] = persons[i + 1]["name"]
        persons[i + 1]["spouse"] = persons[i]["name"]

if __name__ == "__main__":
    data_initialize()

    # Tworzenie losowych osób i dodawanie ich do listy
    persons = [generate_random_person(str(i)) for i in range(1, MAX_RANDOM_PERSONS + 1)]

    # Przypisanie małżeństw
    assign_marriages(persons)

    # Dodawanie osób do zaszyfrowanych plików
    for person_data in persons:
        add_person(person_data)
        print(f"Dodano losową osobę: {person_data['name']}, Małżonek: {person_data['spouse']}")
