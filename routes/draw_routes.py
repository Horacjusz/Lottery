from flask import Blueprint, jsonify, request
from services.draw_service import main_draw
from services.file_service import load_user_file
from settings.tokens import *

draw_blueprint = Blueprint("draw", __name__, template_folder="templates")

@draw_blueprint.route("/draw_assignment/<int:user_id>", methods=["POST"])
def draw_assignment(user_id):
    previous_assignment = load_user_file(user_id)[ASSIGNMENT]
    assignment = main_draw(user_id)
    
    if assignment is None:
        print(f"No new assignment made for user {user_id}. Falling back to previous assignment.")
        assignment = previous_assignment

    assignment_name = None
    if assignment is not None:
        assignment_data = load_user_file(assignment)
        assignment_name = assignment_data[NAME]

    message = f"Assignment for user {user_id}: {assignment or 'None'}."
    print(message)

    return jsonify({
        "success": True,
        "assignment": assignment,
        "assignment_name": assignment_name,
        "message": message,
    })

