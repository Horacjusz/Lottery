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

# from services.user_service import *  # Import necessary services


auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    error_message = ""
    if request.method == "POST":
        username = request.form["username"]
        print(username)
        password = request.form["password"]
        print(password)
        user_id = get_id_from_username(username)
        print(user_id)

        if verify_user(username, password):
            session["username"] = username
            session["user_id"] = user_id
            session["is_admin"] = is_admin(user_id)
            flash("Zalogowano pomyślnie!", "success")

            # Redirect to the appropriate dashboard
            if session["is_admin"] and not is_visible(user_id):
                return redirect(url_for("admin.admin_dashboard"))
            return redirect(url_for("dashboard.dashboard"))
        else:
            error_message = "Nieznany użytkownik lub błędne hasło."

    return render_template("login.html", error_message=error_message)

@auth_blueprint.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("user_id", None)
    flash("Wylogowano pomyślnie!", "success")
    return redirect(url_for("auth.login"))