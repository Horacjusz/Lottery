from flask import Blueprint, jsonify, request
from services.user_functions.user_service import edit_user, check_user_existence, create_user  # Assuming this function exists
from services.file_service import load_user_file
from settings.tokens import *
from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.user_functions.user_service import create_user  # Assuming create_user function exists
from settings.settings import USERS_PATH  # Adjust import paths as needed

user_blueprint = Blueprint("user", __name__, template_folder="templates")

@user_blueprint.route("/update/<int:user_id>", methods=["POST"])
@user_blueprint.route("/update/", methods=["POST"])
def update_user_route(user_id=None):
    """Route to update or create a new user."""
    print(f"Updating user: {user_id}")
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "Invalid JSON payload."}), 400

        new_name = data.get("new_name")
        new_username = data.get("new_username")
        new_password = data.get("new_password")
        new_choosable = data.get("new_choosable", True)
        new_visible = data.get("new_visible", True)
        new_admin = data.get("new_admin", False)
        new_spouse = data.get("new_spouse")
        reset_spouse = False

        if new_spouse == "None":
            new_spouse = None
            reset_spouse = True
        if new_spouse is not None:
            new_spouse = int(new_spouse)

        if not new_name or not new_username or new_password is None:
            return jsonify({"success": False, "error": "Missing required fields."}), 400

        # If `user_id` is None or user doesn't exist, create a new user
        if user_id is None or not check_user_existence(user_id):
            user_id = create_user()

        # Update the user
        edit_user(
            user_id=user_id,
            new_name=new_name,
            new_username=new_username,
            new_password=new_password,
            new_choosable=new_choosable,
            new_visible=new_visible,
            new_admin=new_admin,
            new_spouse=new_spouse,
            reset_spouse=reset_spouse,
        )

        return jsonify({"success": True, "message": "User updated successfully."})
    except Exception as e:
        print(f"Error updating user {user_id}: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@user_blueprint.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Nie przesłano danych w żądaniu JSON"}), 400

    username = data.get("username")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    if not username or not password or not confirm_password:
        return jsonify({"error": "Brakujące dane. Uzupełnij wszystkie pola"}), 400

    if password != confirm_password:
        return jsonify({"error": "Hasła nie są identyczne"}), 400

    if check_user_existence(username):
        return jsonify({"error": "Nazwa użytkownika jest już zajęta"}), 400

    # Tworzenie użytkownika
    create_user(username=username, password=password)
    return jsonify({"message": "Rejestracja przebiegła pomyślnie"}), 201