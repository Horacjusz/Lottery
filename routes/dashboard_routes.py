from flask import session, flash, redirect, url_for, render_template
from services.encryption_service import decrypt_file
from config.settings import USERS_DATA_FILE

# from app import app
from flask import Blueprint, session, request, jsonify, redirect, url_for, render_template, flash
from services.user_service import *  # Import necessary services

dashboard_blueprint = Blueprint("dashboard", __name__)

@dashboard_blueprint.route("/dashboard")
def dashboard():
    if "username" not in session:
        flash("Musisz być zalogowany, aby zobaczyć tę stronę.", "error")
        return redirect(url_for("auth.login"))

    username = session["username"]
    users_data = decrypt_data()
    user_id = session["user_id"]
    user_data = users_data[user_id]

    if user_data is None:
        flash("Nie znaleziono danych użytkownika. Proszę spróbować ponownie.", "error")
        return redirect(url_for("auth.logout"))

    # User's wishlist for the dashboard
    wishlist = user_data.wishlist
    
    # List of reserved items (items reserved by the current user in other users' wishlists)
    reserved_items = [
        {
            "name": item["name"],
            "description": item["description"],
            "owner_name": users_data[owner_id].name,
            "owner_username": users_data[owner_id].username
        }
        for owner_id, data in users_data.items()
        if owner_id != user_id
        # and owner_id != users_data[user_id].assignment  # Exclude assigned user's items
        for item in data.wishlist
        if item["reserved_by"] == user_id
    ]
    
    assigned_user = users_data[user_data.assignment] if user_data.assignment is not None else None

    # print(users_data[user_data.assignment])
    
    return render_template("dashboard.html", username=username, user_id=user_id, wishlist=wishlist, reserved_items=reserved_items, user_data = user_data, assigned_user = assigned_user)
