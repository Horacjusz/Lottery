from flask import Blueprint, jsonify, request, session
from services.user_functions.user_service import edit_user, check_user_existence, create_user  # Assuming this function exists
from services.file_service import load_user_file
from settings.tokens import *
from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.user_functions.user_service import create_user  # Assuming create_user function exists
from settings.settings import load_settings  # Adjust import paths as needed
from services.lists_service import get_available_spouses, get_all_users, get_all_items

user_blueprint = Blueprint("user", __name__, template_folder="templates")

@user_blueprint.route("/update/<int:user_id>", methods=["POST", "GET"])
@user_blueprint.route("/update/", methods=["POST", "GET"])
def update_user_route(user_id=None, edit_mode = False):
    """Route to update or create a new user."""
    print("update_user_route")
    if request.method != "POST":
        return render_template("register.html", user = None, settings = load_settings(), edit_mode = False, user_id = 'new', users_data = get_all_users())
    
    print(f"Updating user: {user_id}")
    print("communicated to backend")
    try:
        print(user_id)
        if user_id == 'new' :
            user_id = None
        
        data = request.get_json()
        print(data)
        if not data:
            return jsonify({"success": False, "error": "Invalid JSON payload."}), 400

        new_name = data.get("new_name", None)
        new_username = data.get("new_username", None)
        new_password = data.get("new_password", None)
        new_choosable = data.get("new_choosable", True)
        new_visible = data.get("new_visible", True)
        new_admin = data.get("new_admin", False)
        new_spouse = data.get("new_spouse", None)
        
        # Handle spouse reset explicitly
        reset_spouse = False
        if new_spouse == "None":
            new_spouse = None
            reset_spouse = True
        if new_spouse is not None:
            try:
                new_spouse = int(new_spouse)
            except ValueError:
                return jsonify({"success": False, "error": "Invalid spouse ID."}), 400
            
        print("check existance of", user_id)
        # If `user_id` is None or user doesn't exist, create a new user
        if user_id is None or not check_user_existence(user_id):
            print(f"user {user_id} does not exist")
            user_id = create_user()[USER_ID]
            print(f"assigned id {user_id}")

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


@user_blueprint.route("/is_username_free", methods=["POST"])
def is_username_free():
    """Endpoint to check if a username is available."""
    data = request.get_json()
    if not data or USERNAME not in data:
        return jsonify({"is_free": False, "error": "Invalid request."}), 400

    username = data[USERNAME]
    users_data = get_all_users()
    is_free = not any(user[USERNAME] == username for user in users_data.values())

    # Odczytujemy parametr edit_mode z query parameters
    edit_mode = request.args.get("edit_mode", "false").lower() == "true"

    if username == OWNER_USERNAME:
        is_free = False

    if edit_mode :
        if (username == session.get(USERNAME)) :
            is_free = True

    print(f"username {username} being free is {is_free}")

    return jsonify({"is_free": is_free})



@user_blueprint.route("/user_list")
def user_list():
    
    user_id = session[USER_ID]
    
    return render_template("user_list.html", users=get_all_users().values(), user_id=user_id, items_data = get_all_items())