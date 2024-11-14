from flask import session, jsonify
from services.draw_service import main_draw
from services.encryption_service import decrypt_file, encrypt_file
from config.settings import DATA_PATH, USERS_DATA_FILE, CHOOSING_FILE, CHOSEN_FILE
import json
import os
# from app import app

from flask import Blueprint, session, request, jsonify, redirect, url_for, render_template, flash
from services.user_service import *  # Import necessary services

draw_blueprint = Blueprint("draw", __name__)

@draw_blueprint.route("/start_draw", methods=["POST"])
def start_draw():
    if "username" not in session or "user_id" not in session:
        return jsonify({"error": "Musisz być zalogowany, aby wykonać tę operację."}), 403

    user_id = session["user_id"]
    

    # Wykonanie losowania
    drawn_person = main_draw(user_id)
    if drawn_person:
        users_data = decrypt_data(True)
        users_data[user_id]["assignment"] = drawn_person
        encrypt_file(json.dumps(users_data, ensure_ascii=False, indent=4), USERS_DATA_FILE)
        drawn_person = User.from_dict(users_data[drawn_person])
        return jsonify({"success": True, "username": drawn_person.username, "name": drawn_person.name, "wishlist": drawn_person.wishlist})
    else:
        return jsonify({"error": "Nie udało się wykonać losowania."}), 500