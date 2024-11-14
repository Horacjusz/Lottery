from flask import session, flash, redirect, url_for, request, render_template, jsonify
from services.encryption_service import decrypt_file, encrypt_file
from config.settings import USERS_DATA_FILE
from services.user_service import update_pool_files, add_to_wishlist, remove_from_wishlist, get_id, verify_username
from services.data_service import data_to_dict
import json

# from app import app
from flask import Blueprint, session, request, jsonify, redirect, url_for, render_template, flash
from services.user_service import *  # Import necessary services

user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/edit_user", methods=["GET", "POST"])
def edit_user():
    if "username" not in session:
        flash("Musisz być zalogowany, aby edytować swoje dane.", "error")
        return redirect(url_for("login"))

    username = session["username"]
    user_id = session["user_id"]
    users_data = decrypt_data()
    user_data = users_data[user_id]

    if not user_data:
        flash("Nie znaleziono danych użytkownika.", "error")
        return redirect(url_for("dashboard.dashboard"))

    # Define available_spouses at the top, so it’s accessible for both GET and POST requests
    available_spouses = [
        {"id": uid, "name": user.name}
        for uid, user in users_data.items()
        if user.spouse is None and user.username != username
    ]

    if request.method == "POST":
        # Pobranie wartości z formularza
        new_choosable = request.form.get("choosable") == "on"
        new_name = request.form["name"]
        new_username = request.form["username"]
        new_password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        spouse_id = request.form.get("spouse")

        # Sprawdzanie, czy hasła się zgadzają
        if new_password and new_password != confirm_password :
                flash("Hasła nie są identyczne. Spróbuj ponownie.", "error")
                return render_template("register.html", user_data=user_data, available_spouses=available_spouses, edit_mode=True, error_message_password="Hasła nie są identyczne, spróbuj ponownie.")

        if new_username != username and not verify_username(new_username) :
                message = "Nazwa użytkownika jest już zajęta."
                flash(message, "error")
                return render_template("register.html", user_data=user_data, available_spouses=available_spouses, edit_mode=True, error_message=message)


        # Update user data
        user_data.choosable = new_choosable
        user_data.name = new_name
        user_data.username = new_username
        if new_password:
            user_data.password = new_password  # Update password only if provided and confirmed
        user_data.spouse = spouse_id if spouse_id != "None" else None

        # Zapis zaktualizowanych danych użytkownika do `users_data`
        users_data[user_id] = user_data

        # Sortowanie i ponowne zaszyfrowanie danych rodziny
        encrypt_file(json.dumps(data_to_dict(users_data), ensure_ascii=False, indent=4), USERS_DATA_FILE)

        # Aktualizacja nazwy użytkownika w sesji, jeśli uległa zmianie
        if new_username != username:
            session["username"] = new_username
            flash("Nazwa użytkownika została zaktualizowana.", "info")

        flash("Dane zostały pomyślnie zaktualizowane!", "success")

        # Przekierowanie do dashboardu po pomyślnej aktualizacji
        return redirect(url_for("dashboard.dashboard"))

    return render_template("register.html", user_data=user_data, available_spouses=available_spouses, edit_mode=True)






@user_blueprint.route("/user_list")
def user_list():
    users_data = decrypt_file(USERS_DATA_FILE)
    username = session.get("username")
    current_user_id = None

    # Find the current user's ID
    for user_id, user_data in users_data.items():
        if user_data["username"] == username:
            current_user_id = user_id
            break

    users_with_wishlists = []
    for user_id, user_data in users_data.items():
        # Skip the current user's own wishlist
        if user_id == current_user_id:
            continue
        
        print(users_data[current_user_id])

        # Filter items based on reservation visibility for the current user
        visible_wishlist = [
            {
                "name": item["name"],
                "description": item["description"],
                "reserved_by": item.get("reserved_by")
            }
            for item in user_data.get("wishlist", [])
            if item.get("reserved_by") is None or item["reserved_by"] == current_user_id
        ]

        # Only include users who have items in their visible wishlist
        if visible_wishlist:
            users_with_wishlists.append({
                "username": user_data["username"],
                "name": user_data["name"],
                "wishlist": visible_wishlist
            })

    return render_template("user_list.html", users=users_with_wishlists, current_user_id=current_user_id)


@user_blueprint.route("/add_wishlist_item", methods=["POST"])
def add_wishlist_item():
    if "username" not in session:
        return jsonify({"error": "Musisz być zalogowany, aby wykonać tę operację."}), 403

    username = session["username"]
    user_id = session["user_id"]
    wishlist_data = request.json
    item_name = wishlist_data.get('wishlist_item')
    item_description = wishlist_data.get('wishlist_description')

    # Log data for debugging
    print(f"Received request to add item: {item_name} with description: {item_description} for user: {username}")

    if item_name:
        success = add_to_wishlist(user_id, item_name, item_description)
        if success:
            return jsonify({"success": True, "item": item_name, "description": item_description}), 200
        else:
            print(f"Error: Could not add item '{item_name}' for user '{username}'.")
            return jsonify({"error": "Nie udało się dodać przedmiotu do listy życzeń."}), 500
    else:
        return jsonify({"error": "Brak przedmiotu do dodania."}), 400
    
    
    
@user_blueprint.route("/remove_wishlist_item", methods=["POST"])
def remove_wishlist_item():
    if "username" not in session:
        return jsonify({"error": "Musisz być zalogowany, aby wykonać tę operację."}), 403

    username = session["username"]
    user_id = session["user_id"]
    item_name = request.json.get("wishlist_item")
    item_description = request.json.get("wishlist_description")

    # Ensure both item_name and item_description are provided
    if item_name and item_description:
        remove_from_wishlist(user_id, item_name, item_description)
        print("removed")
        return jsonify({"success": True, "item": item_name}), 200
    else:
        return jsonify({"error": "Brak przedmiotu lub opisu do usunięcia."}), 400
    
    
    
@user_blueprint.route("/edit_wishlist_item", methods=["POST"])
def edit_wishlist_item():
    if "username" not in session:
        return jsonify({"error": "Musisz być zalogowany, aby wykonać tę operację."}), 403

    username = session["username"]
    data = request.json
    original_name = data.get("original_name")
    original_description = data.get("original_description")
    new_name = data.get("new_name")
    new_description = data.get("new_description")

    users_data = decrypt_file(USERS_DATA_FILE)
    if username in users_data and "wishlist" in users_data[username]:
        wishlist = users_data[username]["wishlist"]

        # Find and update the item based on both name and description
        for i, (name, desc) in enumerate(wishlist):
            if name == original_name and desc == original_description:
                wishlist[i] = (new_name, new_description)
                break

        # Save updated data
        encrypted_data = json.dumps(users_data, ensure_ascii=False, indent=4)
        encrypt_file(encrypted_data, USERS_DATA_FILE)
        return jsonify({"success": True}), 200

    return jsonify({"error": "Przedmiot nie został znaleziony."}), 404


@user_blueprint.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    if "username" not in session:
        flash("Musisz być zalogowany, aby edytować swój profil.", "error")
        return redirect(url_for("login"))
    
    username = session["username"]
    users_data = decrypt_file(USERS_DATA_FILE)
    user_data = next((user for user in users_data.values() if user["username"] == username), None)
    
    if request.method == "POST":
        # Pobranie imienia i nazwiska z formularza
        name = request.form["name"]
        users_data[username]["name"] = name  # Aktualizacja pola "name"
        
        # Zapis danych
        encrypt_file(json.dumps(users_data, ensure_ascii=False, indent=4), USERS_DATA_FILE)
        
        flash("Profil został zaktualizowany.", "success")
        return redirect(url_for("dashboard.dashboard.dashboard"))
    
    return render_template("edit_profile.html", user_data=user_data)



@user_blueprint.route("/approve_wishlist_item", methods=["POST"])
def approve_wishlist_item():
    if "username" not in session:
        return jsonify({"error": "Musisz być zalogowany, aby wykonać tę operację."}), 403

    data = request.json
    username = session["username"]
    users_data = decrypt_file(USERS_DATA_FILE)

    # Find the reserving user's ID
    reserving_user_id = next((id for id, user in users_data.items() if user["username"] == username), None)
    if reserving_user_id is None:
        return jsonify({"error": "Nie znaleziono użytkownika."}), 404

    # Locate the item in the wishlist and update reserved_by
    target_user_id = str(data.get("user_id"))
    item_name = data.get("item_name")
    item_description = data.get("item_description")

    if target_user_id in users_data:
        wishlist = users_data[target_user_id]["wishlist"]
        for item in wishlist:
            if item["name"] == item_name and item["description"] == item_description:
                # Toggle reservation
                if item["reserved_by"] is None:
                    item["reserved_by"] = reserving_user_id
                elif item["reserved_by"] == reserving_user_id:
                    item["reserved_by"] = None
                break

        # Save updated users data to the encrypted file
        encrypted_data = json.dumps(users_data, ensure_ascii=False, indent=4)
        encrypt_file(encrypted_data, USERS_DATA_FILE)
        return jsonify({"success": True}), 200

    return jsonify({"error": "Nie znaleziono przedmiotu do zatwierdzenia."}), 404


@user_blueprint.route("/reserve_wishlist_item", methods=["POST"])
def reserve_wishlist_item():
    if "username" not in session:
        return jsonify({"error": "Musisz być zalogowany, aby wykonać tę operację."}), 403

    data = request.json
    print(data)
    username = session["username"]
    target_username = data.get("username")  # Owner of the wishlist
    item_name = data.get("item_name")
    item_description = data.get("item_description")

    # Decrypt and load users data
    users_data = decrypt_file(USERS_DATA_FILE)
    
    # Locate the current user's ID
    current_user_id = None
    for user_id, user_data in users_data.items():
        if user_data["username"] == username:
            current_user_id = user_id
            break
    
    print("got_here")
    
    # Locate the item in the target user's wishlist and update reservation
    if target_username in [user["username"] for user in users_data.values()]:
        print(target_username,"exists")
        for user_id, user_data in users_data.items():
            if user_data["username"] == target_username:
                print("target name is", user_data["name"])
                for item in user_data["wishlist"]:
                    if item["name"] == item_name and item["description"] == item_description:
                        # Toggle reservation: set to current user ID or None if already reserved by the current user
                        if item.get("reserved_by") != current_user_id:
                            item["reserved_by"] = current_user_id
                            users_data[str(get_id(username))]["reserved_items"].append({"name" : item_name, "description" : item_description})
                            print(f"{username} reserved '{item_name}' from {target_username}'s wishlist.")
                        else:
                            item["reserved_by"] = None
                            users_data[str(get_id(username))]["reserved_items"].remove({"name" : item_name, "description" : item_description})
                            print(f"{username} resigned from reserving '{item_name}' from {target_username}'s wishlist.")
                        print(username)
                        print(users_data[str(get_id(username))]["reserved_items"])
                        break

        # Save updated data
        encrypt_file(json.dumps(users_data, ensure_ascii=False, indent=4), USERS_DATA_FILE)
        return jsonify({"success": True, "message": f"Reservation status updated for {item_name}."}), 200

    return jsonify({"error": "Nie znaleziono przedmiotu do rezerwacji."}), 404