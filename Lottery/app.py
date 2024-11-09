from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import json
import os
from cipher_data import decrypt_file, encrypt_file

app = Flask(__name__)
app.secret_key = 'supersecretkey'

DATA_PATH = os.path.join(os.path.dirname(__file__), "data")
USERS_FILE = os.path.join(DATA_PATH, "users_encrypted")
FAMILY_DATA_FILE = os.path.join(DATA_PATH, "family_data_encrypted")

def verify_user(username, password):
    users_data = decrypt_file(USERS_FILE)
    user_info = users_data.get(username)
    if user_info and user_info["password"] == password:
        return True
    return False

def add_user(username, password):
    try:
        users_data = decrypt_file(USERS_FILE)
    except FileNotFoundError:
        users_data = {}

    if username in users_data:
        return False

    users_data[username] = {"password": password}
    encrypted_data = json.dumps(users_data, ensure_ascii=False, indent=4)
    encrypt_file(encrypted_data, USERS_FILE)
    return True

def get_user_wishlist(username):
    family_data = decrypt_file(FAMILY_DATA_FILE)
    user_data = family_data.get(username, {})
    # Zwraca pełną listę przedmiotów, każdy z nazwą i opisem
    return user_data.get("wishlist", [])

def add_to_wishlist(username, item_name, item_description):
    family_data = decrypt_file(FAMILY_DATA_FILE)
    
    # Sprawdź, czy użytkownik już istnieje w family_data
    if username not in family_data:
        family_data[username] = {"wishlist": {}}

    # Zaktualizuj listę życzeń użytkownika
    family_data[username]["wishlist"][item_name] = item_description

    # Zaszyfruj i zapisz zmiany
    encrypted_data = json.dumps(family_data, ensure_ascii=False, indent=4)
    encrypt_file(encrypted_data, FAMILY_DATA_FILE)


def remove_from_wishlist(username, item_name):
    family_data = decrypt_file(FAMILY_DATA_FILE)
    if username in family_data and "wishlist" in family_data[username]:
        # Znajdź i usuń przedmiot po nazwie
        family_data[username]["wishlist"] = [
            item for item in family_data[username]["wishlist"]
            if item["name"] != item_name
        ]
        encrypted_data = json.dumps(family_data, ensure_ascii=False, indent=4)
        encrypt_file(encrypted_data, FAMILY_DATA_FILE)

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if verify_user(username, password):
            session["username"] = username
            flash("Zalogowano pomyślnie!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Nieprawidłowa nazwa użytkownika lub hasło.", "error")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        new_username = request.form["username"]
        new_password = request.form["password"]

        if add_user(new_username, new_password):
            flash(f"Konto dla {new_username} zostało pomyślnie utworzone!", "success")
            return redirect(url_for("login"))
        else:
            flash("Użytkownik o tej nazwie już istnieje.", "error")

    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        flash("Musisz być zalogowany, aby zobaczyć tę stronę.", "error")
        return redirect(url_for("login"))

    username = session["username"]
    wishlist = get_user_wishlist(username)
    return render_template("dashboard.html", username=username, wishlist=wishlist)

@app.route("/add_wishlist_item", methods=["POST"])
def add_wishlist_item():
    if "username" not in session:
        return jsonify({"error": "Musisz być zalogowany, aby wykonać tę operację."}), 403

    username = session["username"]
    item_name = request.json.get("wishlist_item")
    item_description = request.json.get("wishlist_description", "")

    if item_name:
        add_to_wishlist(username, item_name, item_description)
        return jsonify({"success": True, "item": item_name, "description": item_description}), 200
    else:
        return jsonify({"error": "Brak przedmiotu do dodania."}), 400

@app.route("/remove_wishlist_item", methods=["POST"])
def remove_wishlist_item():
    if "username" not in session:
        return jsonify({"error": "Musisz być zalogowany, aby wykonać tę operację."}), 403

    username = session["username"]
    item_to_remove = request.json.get("wishlist_item")
    if item_to_remove:
        remove_from_wishlist(username, item_to_remove)
        return jsonify({"success": True, "item": item_to_remove}), 200
    else:
        return jsonify({"error": "Brak przedmiotu do usunięcia."}), 400

@app.route("/edit_wishlist_item", methods=["POST"])
def edit_wishlist_item():
    if "username" not in session:
        return jsonify({"error": "Musisz być zalogowany, aby wykonać tę operację."}), 403

    username = session["username"]
    data = request.json
    original_name = data.get("original_name")
    new_name = data.get("new_name")
    new_description = data.get("new_description")

    family_data = decrypt_file(FAMILY_DATA_FILE)
    if username in family_data and "wishlist" in family_data[username]:
        wishlist = family_data[username]["wishlist"]

        # Sprawdź, czy przedmiot istnieje i zaktualizuj jego nazwę i opis
        if original_name in wishlist:
            del wishlist[original_name]  # Usuń stary wpis
            wishlist[new_name] = new_description  # Dodaj nowy wpis

            # Zapisz zmiany
            encrypted_data = json.dumps(family_data, ensure_ascii=False, indent=4)
            encrypt_file(encrypted_data, FAMILY_DATA_FILE)
            return jsonify({"success": True}), 200

    return jsonify({"error": "Przedmiot nie został znaleziony."}), 404




@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Wylogowano pomyślnie!", "success")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
