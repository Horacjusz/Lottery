from flask import Blueprint, jsonify, request, session
from services.user_functions.user_service import edit_user, check_user_existence, create_user
from settings.tokens import *
from flask import Blueprint, render_template, request
from services.user_functions.user_service import create_user, delete_user
from services.file_service import load_settings
from services.lists_service import get_all_users, get_all_items

user_blueprint = Blueprint("user", __name__, template_folder="templates")

@user_blueprint.route("/update", methods=["POST", "GET"])
def update_user_route():
    if request.method != "POST":
        return render_template("register.html", user = None, settings = load_settings(), edit_mode = False, user_id = 'new', users_data = get_all_users())

    try:

        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "Invalid JSON payload."}), 400
        user_id = data.get("user_id", None)
        new_name = data.get("name", None)
        new_username = data.get("username", None)
        new_password = data.get("password", None)
        new_choosable = data.get("choosable", True)
        new_visible = data.get("visible", True)
        new_admin = data.get("admin", False)
        new_spouse = data.get("spouse", None)

        if user_id == 'new' :
            user_id = None

        reset_spouse = False
        if new_spouse == "None":
            new_spouse = None
            reset_spouse = True
        if new_spouse is not None:
            try:
                new_spouse = int(new_spouse)
            except ValueError:
                return jsonify({"success": False, "error": "Invalid spouse ID."}), 400

        if user_id is None or not check_user_existence(user_id):
            user_id = create_user()[USER_ID]

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
        print(f"Error updating user: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@user_blueprint.route("/is_username_free", methods=["POST"])
def is_username_free():
    data = request.get_json()
    if not data or USERNAME not in data:
        return jsonify({"is_free": False, "error": "Invalid request.", "success": True}), 400

    username = data[USERNAME]
    users_data = get_all_users()
    is_free = not any(user[USERNAME] == username for user in users_data.values())

    edit_mode = request.args.get("edit_mode", "false").lower() == "true"

    if username == OWNER_USERNAME:
        is_free = False

    if edit_mode :
        if (username == session.get(USERNAME)) :
            is_free = True

    return jsonify({"is_free": is_free, "success": True})



@user_blueprint.route("/user_list")
def user_list():
    
    user_id = session[USER_ID]
    
    return render_template("user_list.html", users=get_all_users().values(), user_id=user_id, items_data = get_all_items())



@user_blueprint.route('/delete_user_route', methods=['POST'])
def delete_user_route():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        if user_id is None:
            return jsonify({"success": False, "message": "User ID not provided"}), 400

        success = delete_user(user_id)

        if success:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "Could not delete user due to assignment conflicts"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500