import os
import json
import shutil
from settings.settings import USERS_PATH, DATA_PATH
from services.retrieval import user_file_path
from services.retrieval import item_file_path
from settings.tokens import *

def save_user_file(user_data):
    save_json_file(user_file_path(user_data[USER_ID]), user_data)

def load_user_file(user_id):
    return load_json_file(user_file_path(user_id))

def delete_user_file(user_id):
    delete_json_file(user_file_path(user_id))
    
    
def save_item_file(item_data):
    save_json_file(item_file_path(item_data[ITEM_ID]), item_data)

def load_item_file(item_id):
    return load_json_file(item_file_path(item_id))

def delete_item_file(item_id):
    delete_json_file(item_file_path(item_id))
    
    
def load_json_file(file_path) :
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist.")
    
    with open(file_path, 'r') as file:
        try:
            return json.load(file) 
        except json.JSONDecodeError:
            file.seek(0)
            return file.read()
        
def save_json_file(file_path, content) :
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if isinstance(content, dict):
        with open(file_path, 'w') as file:
            json.dump(content, file, indent=4)
    elif isinstance(content, str):
        with open(file_path, 'w') as file:
            file.write(content)
    else:
        raise ValueError("User data must be a dictionary or a string.")

def delete_file(path) :
    if not os.path.exists(path):
        raise FileNotFoundError(f"File {path} does not exist.")
    if os.path.isfile(path) or os.path.islink(path):
        os.unlink(path)  # Remove file or symlink
    elif os.path.isdir(path):
        shutil.rmtree(path)  # Remove directory and its contents

def delete_json_file(file_path) :
    # if not os.path.exists(file_path):
    #     raise FileNotFoundError(f"File {file_path} does not exist.")
    # os.remove(file_path)
    delete_file(file_path)

# Clear the data directory
def clear_directory(dirname):
    """
    Clear all contents of the data directory, including subdirectories and files.

    Returns:
        None
    """
    for item in os.listdir(dirname):
        item_path = os.path.join(dirname, item)
        delete_file(item_path)
    print(f"Cleared all contents of the data directory: {DATA_PATH}")

def test_file_service():
    pass

