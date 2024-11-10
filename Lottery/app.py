from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import json
import os
from cipher_data import decrypt_file, encrypt_file
from data_create import add_person
from main_code import main_draw
from copy import deepcopy

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecretkey")

DATA_PATH = os.path.join(os.path.dirname(__file__), "data")
FAMILY_DATA_FILE = os.path.join(DATA_PATH, "family_data_encrypted")
CHOSEN_FILE = os.path.join(DATA_PATH, "chosen_encrypted")
CHOOSING_FILE = os.path.join(DATA_PATH, "choosing_encrypted")

def verify_user(username, password):
    family_data = decrypt_file(FAMILY_DATA_FILE)
    print(family_data)
    for user in family_data.values():
        if user["username"] == username and user["password"] == password:
            return True
    return False

def get_id(username) :
    family_data = decrypt_file(FAMILY_DATA_FILE)
    for user in family_data.values():
        if user["username"] == username:
            return user["id"]


def update_pool_files(family_data):
    """
    Updates the choosing and chosen files with users marked as choosable.
    """
    
    choosing_data = deepcopy(family_data)
    chosen_data = deepcopy(family_data)

    # Encrypt and save updated choosing and chosen data
    encrypt_file(json.dumps(choosing_data, ensure_ascii=False, indent=4), CHOOSING_FILE)
    encrypt_file(json.dumps(chosen_data, ensure_ascii=False, indent=4), CHOSEN_FILE)


# Funkcja weryfikująca poprawność i zgodność haseł
def validate_passwords(password, confirm_password):
    if password != confirm_password:
        flash("Hasła nie są zgodne.", "error")
        return False
    return True


def add_user(user_data):
    
    print("Adding user")
    
    family_data = decrypt_file(FAMILY_DATA_FILE)
    
    # Generate a new unique integer ID for each user
    new_id = max([int(key) for key in family_data.keys()], default=0) + 1
    user_data["id"] = new_id
    user_data["reserved_items"] = []  # Initialize reserved items
    user_data["choosable"] = user_data.get("choosable", True)  # Domyślnie True
    user_data["wishlist"] = [
        {"name": item["name"], "description": item["description"], "reserved_by": None} 
        for item in user_data.get("wishlist", [])
    ]
    
    family_data[new_id] = user_data
    update_pool_files(family_data)

    # Encrypt and save updated data
    encrypted_data = json.dumps(family_data, ensure_ascii=False, indent=4)
    encrypt_file(encrypted_data, FAMILY_DATA_FILE)
    # Encrypt and save updated data
    encrypted_data = json.dumps(family_data, ensure_ascii=False, indent=4)
    encrypt_file(encrypted_data, FAMILY_DATA_FILE)
    return True





def get_user_wishlist(user_id):
    """
    Retrieves the wishlist for a user based on their unique ID.
    Only shows items that are either unreserved or reserved by the user themselves.
    """
    family_data = decrypt_file(FAMILY_DATA_FILE)
    user_data = family_data.get(str(user_id))
    if not user_data:
        return []

    return [
        item for item in user_data.get("wishlist", [])
        if item["reserved_by"] is None or item["reserved_by"] == user_id
    ]





def add_to_wishlist(user_id, item_name, item_description):
    family_data = decrypt_file(FAMILY_DATA_FILE)
    
    print(user_id)
    
    if str(user_id) not in family_data:
        return False  # User not found
    
    family_data[str(user_id)]["wishlist"].append({
        "name": item_name,
        "description": item_description,
        "reserved_by": None  # Set reserved_by to None initially
    })

    # Encrypt and save updated data
    encrypted_data = json.dumps(family_data, ensure_ascii=False, indent=4)
    encrypt_file(encrypted_data, FAMILY_DATA_FILE)
    return True




    
def remove_from_wishlist(user_id, item_name, item_description):
    family_data = decrypt_file(FAMILY_DATA_FILE)

    if str(user_id) in family_data and "wishlist" in family_data[str(user_id)]:
        
        reservationist = None
        for userID in family_data :
            if userID == str(user_id) :
                for item in family_data[userID]["wishlist"] :
                    if item["name"] == item_name and item["description"] :
                        reservationist = item["reserved_by"]
                        break
                break
        if reservationist is not None :
            family_data[reservationist]["reserved_items"].remove({"name" : item_name, "description" : item_description})
        
        wishlist = family_data[str(user_id)]["wishlist"]
        family_data[str(user_id)]["wishlist"] = [
            item for item in wishlist if not (item["name"] == item_name and item["description"] == item_description)
        ]
        
            

        # Encrypt and save updated data
        encrypted_data = json.dumps(family_data, ensure_ascii=False, indent=4)
        encrypt_file(encrypted_data, FAMILY_DATA_FILE)



def get_available_spouses(family_data, exclude=None):
    """
    Returns a list of available spouses (users without a spouse) excluding the specified user by username.
    """
    return [
        {"id": user_id, "name": user.get("name", "Unknown")}
        for user_id, user in family_data.items()
        if user.get("spouse") is None and user.get("username") != exclude
    ]



@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    error_message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_id = get_id(username)
        if verify_user(username, password):
            print("verify passed")
            session["username"] = username
            session["user_id"] = user_id
            print("Zalogowano pomyślnie!", "success")
            flash("Zalogowano pomyślnie!", "success")
            return redirect(url_for("dashboard"))
        else:
            error_message = "Nieznany użytkownik lub błędne hasło."  # Set error message for invalid login

    return render_template("login.html", error_message=error_message)



@app.route("/register", methods=["GET", "POST"])
def register():
    family_data = decrypt_file(FAMILY_DATA_FILE)
    edit_mode = False  # Ensure edit_mode is always False for new registration
    username_exists = False
    error_message = ""

    # Determine if the user is in edit mode
    if "username" in session and request.args.get("edit") == "1":
        edit_mode = True
        username = session["username"]
        user_data = family_data.get(username, {})
        current_spouse_id = user_data.get("spouse")
    else:
        user_data = {}
        current_spouse_id = None

    # Get the list of available spouses, excluding the current user
    available_spouses = get_available_spouses(family_data, exclude=user_data.get("username"))

    if request.method == "POST":
        # Capture form values to retain them in case of an error
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        name = request.form["name"]
        choosable = request.form.get("choosable") == "on"
        spouse_id = request.form.get("spouse")
        new_id = max([int(key) for key in family_data.keys()], default=0) + 1
        assignment = None

        # Check if the passwords match
        if not validate_passwords(password, confirm_password):
            error_message = "Hasła nie są zgodne."
            return render_template("register.html", available_spouses=available_spouses, username_exists=username_exists, error_message=error_message, user_data={"username": username, "name": name, "spouse": spouse_id}, edit_mode=edit_mode)

        # Check if the username already exists (when registering or changing username)
        if not edit_mode or username != session.get("username"):
            if any(user.get("username") == username for user in family_data.values()):
                username_exists = True
                error_message = "Nazwa użytkownika jest już zajęta."
                return render_template("register.html", available_spouses=available_spouses, username_exists=username_exists, error_message=error_message, user_data={"username": username, "name": name, "spouse": spouse_id}, edit_mode=edit_mode)

        # Update or create user data
        if edit_mode:
            # Update existing user data
            user_data["name"] = name
            user_data["spouse"] = None if spouse_id == "None" else spouse_id
            if password:
                user_data["password"] = password  # Update password if provided
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
        # print(max([int(key) for key in ], default=0) + 1)
        print(family_data.keys())
        print(user_data)

        # Update spouse information if applicable
        if spouse_id and spouse_id != "None" and spouse_id in family_data:
            family_data[spouse_id]["spouse"] = username
        # Save the updated family data
        family_data[new_id] = user_data
        update_pool_files(family_data)
        encrypt_file(json.dumps(family_data, ensure_ascii=False, indent=4), FAMILY_DATA_FILE)

        flash("Rejestracja przebiegła pomyślnie! Możesz się teraz zalogować.", "success")

        # Redirect to the login page after successful registration
        return redirect(url_for("login"))

    return render_template("register.html", available_spouses=available_spouses, username_exists=username_exists, error_message=error_message, user_data=user_data, edit_mode=edit_mode)












@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        flash("Musisz być zalogowany, aby zobaczyć tę stronę.", "error")
        return redirect(url_for("login"))

    username = session["username"]
    family_data = decrypt_file(FAMILY_DATA_FILE)
    user_data = None
    current_user_id = None

    # Find user data and ID
    for user_id, data in family_data.items():
        if data["username"] == username:
            user_data = data
            current_user_id = user_id
            break

    if user_data is None:
        flash("Nie znaleziono danych użytkownika. Proszę spróbować ponownie.", "error")
        return redirect(url_for("logout"))

    # User's wishlist for the dashboard
    wishlist = user_data.get("wishlist", [])

    # List of reserved items (items reserved by the current user in other users' wishlists)
    reserved_items = [
        {
            "name": item["name"],
            "description": item["description"],
            "owner_name": family_data[owner_id]["name"],
            "owner_username": family_data[owner_id]["username"]
        }
        for owner_id, data in family_data.items()
        if owner_id != current_user_id
        and owner_id != str(family_data[current_user_id].get("assignment"))  # Exclude assigned user's items
        for item in data.get("wishlist", [])
        if item.get("reserved_by") == current_user_id
    ]
    
    assigned_user = None
    
    if user_data["assignment"] is not None :
        assigned_user = family_data[str(user_data["assignment"])]

    return render_template("dashboard.html", username=username, user_id=user_id, wishlist=wishlist, reserved_items=reserved_items, user_data = user_data, assigned_user = assigned_user)







@app.route("/edit_user", methods=["GET", "POST"])
def edit_user():
    if "username" not in session:
        flash("Musisz być zalogowany, aby edytować swoje dane.", "error")
        return redirect(url_for("login"))

    username = session["username"]
    family_data = decrypt_file(FAMILY_DATA_FILE)
    
    # Znajdź `user_id` oraz `user_data` na podstawie `username`
    user_id = next((id for id, user in family_data.items() if user["username"] == username), None)
    user_data = family_data.get(user_id) if user_id else None

    if not user_data:
        flash("Nie znaleziono danych użytkownika.", "error")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        # Pobranie wartości z formularza
        new_choosable = request.form.get("choosable") == "on"
        new_name = request.form["name"]
        new_username = request.form["username"]
        new_password = request.form.get("password")
        spouse_id = request.form.get("spouse")
        confirm_password = request.form.get("confirm_password")

        # Update user data
        user_data["choosable"] = new_choosable
        user_data["name"] = new_name
        user_data["username"] = new_username
        if new_password and new_password == confirm_password:
            user_data["password"] = new_password  # Update password only if provided and confirmed
        user_data["spouse"] = spouse_id if spouse_id != "None" else None

        # Zapis zaktualizowanych danych użytkownika do `family_data`
        family_data[user_id] = user_data

        # Sortowanie i ponowne zaszyfrowanie danych rodziny
        family_data = dict(sorted(family_data.items(), key=lambda x: x[1]["name"]))
        update_pool_files(family_data)
        encrypt_file(json.dumps(family_data, ensure_ascii=False, indent=4), FAMILY_DATA_FILE)

        # Aktualizacja nazwy użytkownika w sesji, jeśli uległa zmianie
        if new_username != username:
            session["username"] = new_username
            flash("Nazwa użytkownika została zaktualizowana.", "info")

        flash("Dane zostały pomyślnie zaktualizowane!", "success")
        
        # Przekierowanie do dashboardu po pomyślnej aktualizacji
        return redirect(url_for("dashboard"))

    # Tworzenie listy opcji dla małżonków
    available_spouses = [
        {"id": uid, "name": user["name"]}
        for uid, user in family_data.items()
        if user["spouse"] is None and user["username"] != username
    ]

    return render_template("register.html", user_data=user_data, available_spouses=available_spouses, edit_mode=True)










@app.route("/user_list")
def user_list():
    family_data = decrypt_file(FAMILY_DATA_FILE)
    username = session.get("username")
    current_user_id = None

    # Find the current user's ID
    for user_id, user_data in family_data.items():
        if user_data["username"] == username:
            current_user_id = user_id
            break

    users_with_wishlists = []
    for user_id, user_data in family_data.items():
        # Skip the current user's own wishlist
        if user_id == current_user_id:
            continue
        
        print(family_data[current_user_id])

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














@app.route("/add_wishlist_item", methods=["POST"])
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




@app.route("/remove_wishlist_item", methods=["POST"])
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


@app.route("/edit_wishlist_item", methods=["POST"])
def edit_wishlist_item():
    if "username" not in session:
        return jsonify({"error": "Musisz być zalogowany, aby wykonać tę operację."}), 403

    username = session["username"]
    data = request.json
    original_name = data.get("original_name")
    original_description = data.get("original_description")
    new_name = data.get("new_name")
    new_description = data.get("new_description")

    family_data = decrypt_file(FAMILY_DATA_FILE)
    if username in family_data and "wishlist" in family_data[username]:
        wishlist = family_data[username]["wishlist"]

        # Find and update the item based on both name and description
        for i, (name, desc) in enumerate(wishlist):
            if name == original_name and desc == original_description:
                wishlist[i] = (new_name, new_description)
                break

        # Save updated data
        encrypted_data = json.dumps(family_data, ensure_ascii=False, indent=4)
        encrypt_file(encrypted_data, FAMILY_DATA_FILE)
        return jsonify({"success": True}), 200

    return jsonify({"error": "Przedmiot nie został znaleziony."}), 404

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Wylogowano pomyślnie!", "success")
    return redirect(url_for("login"))

@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    if "username" not in session:
        flash("Musisz być zalogowany, aby edytować swój profil.", "error")
        return redirect(url_for("login"))
    
    username = session["username"]
    family_data = decrypt_file(FAMILY_DATA_FILE)
    user_data = next((user for user in family_data.values() if user["username"] == username), None)
    
    if request.method == "POST":
        # Pobranie imienia i nazwiska z formularza
        name = request.form["name"]
        family_data[username]["name"] = name  # Aktualizacja pola "name"
        
        # Zapis danych
        encrypt_file(json.dumps(family_data, ensure_ascii=False, indent=4), FAMILY_DATA_FILE)
        
        flash("Profil został zaktualizowany.", "success")
        return redirect(url_for("dashboard"))
    
    return render_template("edit_profile.html", user_data=user_data)

@app.route("/verify_password", methods=["GET", "POST"])
def verify_password():
    if "username" not in session:
        flash("Musisz być zalogowany, aby edytować swoje dane.", "error")
        return redirect(url_for("login"))

    if request.method == "POST":
        password = request.form["password"]
        username = session["username"]
        
        # Weryfikacja hasła
        family_data = decrypt_file(FAMILY_DATA_FILE)
        user_data = next((user for user in family_data.values() if user["username"] == username), None)
        
        if user_data and user_data["password"] == password:
            # Przechowywanie informacji o weryfikacji hasła w sesji
            session["verified_for_edit"] = True
            return redirect(url_for("edit_user"))

        # Jeśli hasło jest nieprawidłowe
        return render_template("verify_password.html", error="Nieprawidłowe hasło.")

    return render_template("verify_password.html")


@app.route("/approve_wishlist_item", methods=["POST"])
def approve_wishlist_item():
    if "username" not in session:
        return jsonify({"error": "Musisz być zalogowany, aby wykonać tę operację."}), 403

    data = request.json
    username = session["username"]
    family_data = decrypt_file(FAMILY_DATA_FILE)

    # Find the reserving user's ID
    reserving_user_id = next((id for id, user in family_data.items() if user["username"] == username), None)
    if reserving_user_id is None:
        return jsonify({"error": "Nie znaleziono użytkownika."}), 404

    # Locate the item in the wishlist and update reserved_by
    target_user_id = str(data.get("user_id"))
    item_name = data.get("item_name")
    item_description = data.get("item_description")

    if target_user_id in family_data:
        wishlist = family_data[target_user_id]["wishlist"]
        for item in wishlist:
            if item["name"] == item_name and item["description"] == item_description:
                # Toggle reservation
                if item["reserved_by"] is None:
                    item["reserved_by"] = reserving_user_id
                elif item["reserved_by"] == reserving_user_id:
                    item["reserved_by"] = None
                break

        # Save updated family data to the encrypted file
        encrypted_data = json.dumps(family_data, ensure_ascii=False, indent=4)
        encrypt_file(encrypted_data, FAMILY_DATA_FILE)
        return jsonify({"success": True}), 200

    return jsonify({"error": "Nie znaleziono przedmiotu do zatwierdzenia."}), 404


@app.route("/reserve_wishlist_item", methods=["POST"])
def reserve_wishlist_item():
    if "username" not in session:
        return jsonify({"error": "Musisz być zalogowany, aby wykonać tę operację."}), 403

    data = request.json
    print(data)
    username = session["username"]
    target_username = data.get("username")  # Owner of the wishlist
    item_name = data.get("item_name")
    item_description = data.get("item_description")

    # Decrypt and load family data
    family_data = decrypt_file(FAMILY_DATA_FILE)
    
    # Locate the current user's ID
    current_user_id = None
    for user_id, user_data in family_data.items():
        if user_data["username"] == username:
            current_user_id = user_id
            break
    
    print("got_here")
    
    # Locate the item in the target user's wishlist and update reservation
    if target_username in [user["username"] for user in family_data.values()]:
        print(target_username,"exists")
        for user_id, user_data in family_data.items():
            if user_data["username"] == target_username:
                print("target name is", user_data["name"])
                for item in user_data["wishlist"]:
                    if item["name"] == item_name and item["description"] == item_description:
                        # Toggle reservation: set to current user ID or None if already reserved by the current user
                        if item.get("reserved_by") != current_user_id:
                            item["reserved_by"] = current_user_id
                            family_data[str(get_id(username))]["reserved_items"].append({"name" : item_name, "description" : item_description})
                            print(f"{username} reserved '{item_name}' from {target_username}'s wishlist.")
                        else:
                            item["reserved_by"] = None
                            family_data[str(get_id(username))]["reserved_items"].remove({"name" : item_name, "description" : item_description})
                            print(f"{username} resigned from reserving '{item_name}' from {target_username}'s wishlist.")
                        print(username)
                        print(family_data[str(get_id(username))]["reserved_items"])
                        break

        # Save updated data
        encrypt_file(json.dumps(family_data, ensure_ascii=False, indent=4), FAMILY_DATA_FILE)
        return jsonify({"success": True, "message": f"Reservation status updated for {item_name}."}), 200

    return jsonify({"error": "Nie znaleziono przedmiotu do rezerwacji."}), 404



@app.route("/start_draw", methods=["POST"])
def start_draw():
    if "username" not in session or "user_id" not in session:
        return jsonify({"error": "Musisz być zalogowany, aby wykonać tę operację."}), 403

    user_id = session["user_id"]

    # Ścieżki do plików
    family_data_path = os.path.join(DATA_PATH, "family_data_encrypted")
    pool_files_paths = [CHOOSING_FILE, CHOSEN_FILE]
    assignment_path = os.path.join(DATA_PATH, "assignment_encrypted")

    # Wykonanie losowania
    drawn_person = main_draw(str(user_id), family_data_path, pool_files_paths, assignment_path)
    if drawn_person:
        family_data = decrypt_file(FAMILY_DATA_FILE)
        family_data[str(user_id)]["assignment"] = drawn_person["id"]
        encrypt_file(json.dumps(family_data, ensure_ascii=False, indent=4), FAMILY_DATA_FILE)
        return jsonify({"success": True, "name": drawn_person["name"], "wishlist": drawn_person.get("wishlist", [])})
    else:
        return jsonify({"error": "Nie udało się wykonać losowania."}), 500



if __name__ == "__main__":
    app.run(debug=True)
