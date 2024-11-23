from flask import Blueprint, request, session, jsonify, redirect, url_for, flash, render_template
from flask import Blueprint, render_template, session, redirect, url_for, flash, jsonify, request
from services.verification import is_visible
from services.file_service import load_settings, save_settings
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
        password = request.form[PASSWORD]
        print(password)
        
        if USERNAME in session:
            print("sesja", session)
            flash("Twoja sesja wygasła. Zaloguj się ponownie.", "warning")
            session.pop(USERNAME)
            session.pop(ADMIN)
            session.pop(USER_ID)
            return redirect(url_for("auth.login"))

        if verify_user(username, password):
            user_id = get_id_from_username(username)
            print(user_id)
            session[USERNAME] = username
            session[USER_ID] = user_id
            session[ADMIN] = is_admin(user_id)
            session.permanent = True  # Ustawienie sesji jako trwałej
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

@auth_blueprint.route("/verify_password", methods=["GET", "POST"])
def verify_password() :
    if "username" not in session:
        flash("Musisz być zalogowany, aby edytować swoje dane.", "error")
        return redirect(url_for("auth.login"))
    
    if request.method != "POST" :
        print()
        return render_template("verify_password.html", error="")
    
    user_id = session[USER_ID]
    
    password = request.form[PASSWORD]
    
    user_data = load_user_file(user_id)
    
    user_password = user_data[PASSWORD]
    
    if password != user_password :
        print("Wrong")
        return render_template("verify_password.html", error="Nieprawidłowe hasło.")
    
    return render_template("register.html", user = user_data, settings = load_settings(), edit_mode = True, user_id = user_id, users_data = get_all_users())