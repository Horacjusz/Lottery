from flask import Blueprint, jsonify, request
from services.draw_service import main_draw
from services.file_service import load_user_file
from settings.tokens import *

draw_blueprint = Blueprint("draw", __name__, template_folder="templates")

@draw_blueprint.route("/draw_assignment/<int:user_id>", methods=["POST"])
def draw_assignment(user_id):
    # Load the user's existing data
    previous_assignment = load_user_file(user_id)[ASSIGNMENT]  # Fetch previous assignment if it exists
    # Attempt to make a new assignment
    assignment = main_draw(user_id)
    

    # If no new assignment was made, use the previous assignment
    if assignment is None:
        print(f"No new assignment made for user {user_id}. Falling back to previous assignment.")
        assignment = previous_assignment

    # Load the name of the assigned user (if any)
    assignment_name = None
    if assignment is not None:
        assignment_data = load_user_file(assignment)
        assignment_name = assignment_data[NAME]  # Use "Unknown Name" if NAME is missing

    # Prepare the response
    message = f"Assignment for user {user_id}: {assignment or 'None'}."
    print(message)

    return jsonify({
        "success": True,
        "assignment": assignment,
        "assignment_name": assignment_name,
        "message": message,
    })

