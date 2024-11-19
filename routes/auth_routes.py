from flask import Blueprint, request, session, jsonify, redirect, url_for, flash, render_template
# from services.user_service import get_id, verify_user, is_admin
# from config.settings import USERS_DATA_FILE
# from services.encryption_service import decrypt_file, encrypt_file, update_pool_files
# from services.user_service import get_available_spouses
# from services.user_service import validate_passwords
# from services.data_service import data_to_dict, print_data
# from services.data_service import load_settings
import json

from services.verification import *
from settings.tokens import *

# from services.user_service import *  # Import necessary services


auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    error_message = ""
    if request.method == "POST":
        username = request.form[USERNAME]
        print(username)
        password = request.form["password"]
        print(password)
        user_id = get_id_from_username(username)
        print(user_id)

        if verify_user(username, password):
            session[USERNAME] = username
            session[USER_ID] = user_id
            session[ADMIN] = is_admin(user_id)
            flash("Zalogowano pomyślnie!", "success")

            # Redirect to the appropriate dashboard
            if session[ADMIN] and not is_visible(user_id):
                return redirect(url_for("admin.admin_dashboard"))
            return redirect(url_for("dashboard.dashboard"))
        else:
            error_message = "Nieznany użytkownik lub błędne hasło."

    return render_template("login.html", error_message=error_message)

@auth_blueprint.route("/logout")
def logout():
    session.pop(USERNAME, None)
    session.pop(USER_ID, None)
    flash("Wylogowano pomyślnie!", "success")
    return redirect(url_for("auth.login"))

# @auth_blueprint.route("/verify_password", methods=["GET", "POST"])
# def verify_password() :
#     if "username" not in session:
#         flash("Musisz być zalogowany, aby edytować swoje dane.", "error")
#         return redirect(url_for("auth.login"))
    
    
#     return render_template("verify_password.html", error="Nieprawidłowe hasło.")

@auth_blueprint.route("/register")
def register() :
    _