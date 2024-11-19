from flask import Blueprint, jsonify, request
from services.user_functions.user_service import edit_user  # Assuming this function exists

user_blueprint = Blueprint("user", __name__, template_folder="templates")

@user_blueprint.route("/update/<int:user_id>", methods=["POST"])
def update_user_route(user_id):
    """Route to update user information."""
    print("Updating user", user_id)
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "Invalid JSON payload."}), 400
        
        # Extract fields from the JSON payload
        new_name = data.get("new_name")
        new_username = data.get("new_username")
        new_password = data.get("new_password")
        new_choosable = data.get("new_choosable")
        new_visible = data.get("new_visible")
        new_admin = data.get("new_admin")
        new_spouse = data.get("new_spouse")  # Can be None

        # Ensure all necessary parameters are provided
        if not new_name or not new_username or new_password is None:
            return jsonify({"success": False, "error": "Missing required fields."}), 400

        # Call the service to update the user
        edit_user(
            user_id,
            new_name=new_name,
            new_username=new_username,
            new_password=new_password,
            new_choosable=new_choosable,
            new_visible=new_visible,
            new_admin=new_admin,
            new_spouse=new_spouse,
        )

        return jsonify({"success": True, "message": "User updated successfully."})
    except Exception as e:
        print(f"Error updating user {user_id}: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# @user_blueprint.route("/user_list")
# def user_list():
    