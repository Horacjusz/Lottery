from services.user_functions.user_service import create_user
from settings.tokens import *

def generate_owner() :
    create_user({USER_ID: 0, ADMIN: True, VISIBLE: False, USERNAME: OWNER_USERNAME, PASSWORD: "master_password", NAME: "Admin"})