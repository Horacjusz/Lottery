from flask import Blueprint, jsonify, request
from services.draw_service import main_draw
from services.file_service import load_user_file
from settings.tokens import *

draw_blueprint = Blueprint("draw", __name__, template_folder="templates")

@draw_blueprint.route("/draw_assignment/<int:user_id>", methods=["POST"])
def draw_assignment(user_id):
    assignment = main_draw(user_id)
    
    if assignment is not None:
        print(f"Successfully assigned {assignment} to {user_id}")
        message = f"Assigned {assignment} to user {user_id}."
    else:
        print(f"No assignment made for user {user_id}.")
        message = f"No assignment was made for user {user_id}."
    assignment_name = None
    if assignment is not None :
        assignment_name = load_user_file(assignment)[NAME]
    
    return jsonify({
        "success": True,
        "assignment": assignment,
        "assignment_name": assignment_name,
        "message": message
    })
