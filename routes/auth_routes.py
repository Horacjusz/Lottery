from flask import Blueprint, request, session, jsonify, redirect, url_for, flash, render_template
from flask import Blueprint, render_template, session, redirect, url_for, flash, jsonify, request
from services.verification import is_visible
from settings.settings import load_settings, save_settings
from services.lists_service import get_available_spouses, get_all_users, get_all_items
from settings.tokens import *
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
    return render_template("/register.html", settings = load_settings(), user = None, available_spouses = get_available_spouses(), users_data = get_all_users(), edit_mode = False, admin = False)