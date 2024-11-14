from flask import request, session, redirect, url_for, flash, render_template
from services.user_service import get_id, verify_user
from config.settings import USERS_DATA_FILE
from services.encryption_service import decrypt_file, encrypt_file, update_pool_files
from services.user_service import get_available_spouses
from services.user_service import validate_passwords
from services.data_service import data_to_dict, print_data
import json
# from app import app

from flask import Blueprint, session, request, jsonify, redirect, url_for, render_template, flash
from services.user_service import *  # Import necessary services

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("/")
def home():
    return redirect(url_for("auth.login"))


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    error_message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_id = get_id(username)
        # print(username, password)
        if verify_user(username, password):
            print("verify passed")
            session["username"] = username
            session["user_id"] = user_id
            # print("Zalogowano pomyślnie!", "success")
            flash("Zalogowano pomyślnie!", "success")
            # print_data(user_id)
            return redirect(url_for("dashboard.dashboard"))
        else:
            error_message = "Nieznany użytkownik lub błędne hasło."  # Set error message for invalid login

    return render_template("login.html", error_message=error_message)


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    users_data = decrypt_data()
    # print("Register route accessed")
    # if request.method == "POST":
    #     print("POST")

    edit_mode = False  # Ensure edit_mode is always False for new registration
    username_exists = False
    error_message = ""

    # Determine if the user is in edit mode
    if "username" in session and request.args.get("edit") == "1":
        edit_mode = True
        username = session["username"]
        user_id = session["user_id"]
        # print("username in session", username, user_id)
        user_data = users_data.get(user_id)
    else:
        user_data = User()

    # Get the list of available spouses, excluding the current user
    available_spouses = get_available_spouses(users_data, exclude=user_data.username)

    if request.method == "POST":
        # print("POST")
        # Capture form values to retain them in case of an error
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        name = request.form["name"]
        choosable = request.form.get("choosable") == "on"
        spouse_id = request.form.get("spouse")
        new_id = str(max([int(key) for key in users_data.keys()], default=0) + 1)
        assignment = None

        # Check if the passwords match
        if not validate_passwords(password, confirm_password):
            error_message = "Hasła nie są zgodne."
            return render_template("register.html", available_spouses=available_spouses, username_exists=username_exists, error_message=error_message, user_data={"username": username, "name": name, "spouse": spouse_id}, edit_mode=edit_mode)

        # Check if the username already exists (when registering or changing username)
        if not edit_mode or username != session.get("username"):
            if any(user.username == username for user in users_data.values()):
                username_exists = True
                error_message = "Nazwa użytkownika jest już zajęta."
                return render_template("register.html", available_spouses=available_spouses, username_exists=username_exists, error_message=error_message, user_data={"username": username, "name": name, "spouse": spouse_id}, edit_mode=edit_mode)
        # print(edit_mode)
        # Update or create user data
        if edit_mode:
            # Update existing user data
            user_data.name = name
            user_data.spouse = None if spouse_id == "None" else spouse_id
            if password:
                user_data.password = password  # Update password if provided
        else:
            # Create a new user entry for registration
            user_data = {
                "id": new_id,
                "choosable": choosable,
                "username": username,
                "password": password,
                "name": name,
                "spouse": None if spouse_id == "None" else spouse_id,
                "wishlist": [],
                "reserved_items": [],
                "assignment" : assignment
            }
            # print("username", username)
            # print("password", password)
            user_data = User.from_dict(user_data)
        # print(max([int(key) for key in ], default=0) + 1)
        # print(user_data)

        # Update spouse information if applicable
        if spouse_id and spouse_id != "None" and spouse_id in users_data:
            users_data[spouse_id].spouse = new_id
        # Save the updated users data
        users_data[new_id] = user_data
        # update_pool_files(users_data)
        encrypt_data(json.dumps(data_to_dict(users_data), ensure_ascii=False, indent=4))

        flash("Rejestracja przebiegła pomyślnie! Możesz się teraz zalogować.", "success")

        # Redirect to the login page after successful registration
        return redirect(url_for("auth.login"))

    return render_template("register.html", available_spouses=available_spouses, username_exists=username_exists, error_message=error_message, user_data=user_data, edit_mode=edit_mode)



@auth_blueprint.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("user_id", None)
    flash("Wylogowano pomyślnie!", "success")
    return redirect(url_for("auth.login"))


@auth_blueprint.route("/verify_password", methods=["GET", "POST"])
def verify_password():
    if "username" not in session:
        flash("Musisz być zalogowany, aby edytować swoje dane.", "error")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        password = request.form["password"]
        username = session["username"]
        user_id = session["user_id"]
        
        # Weryfikacja hasła
        users_data = decrypt_data()
        user_data = users_data[user_id] #next((user for user in users_data.values() if user.username == username), None)
        
        if user_data and user_data.password == password:
            # Przechowywanie informacji o weryfikacji hasła w sesji
            session["verified_for_edit"] = True
            return redirect(url_for("user.edit_user"))

        # Jeśli hasło jest nieprawidłowe
        return render_template("verify_password.html", error="Nieprawidłowe hasło.")

    return render_template("verify_password.html")