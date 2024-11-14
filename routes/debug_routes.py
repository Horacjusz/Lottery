from flask import redirect, url_for
from services.file_service import clear_directory  # Adjust if in a different file
from services.data_service import main  # Adjust path if needed
from config.settings import DATA_PATH

# from app import app
from flask import Blueprint, session, request, jsonify, redirect, url_for, render_template, flash
from services.user_service import *  # Import necessary services

debug_blueprint = Blueprint("debug", __name__)

@debug_blueprint.route("/restart_debug", methods=["GET"]) #DO DEBUGU POTEM USUNĄĆ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def restart():
    print("restarting")
    clear_directory(DATA_PATH)
    main()
    return redirect(url_for("auth.login"))