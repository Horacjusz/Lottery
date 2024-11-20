from flask import Blueprint, render_template, session, redirect, url_for, flash, jsonify, request
from services.verification import is_visible
from settings.settings import load_settings, save_settings
from services.lists_service import get_available_spouses, get_all_users, get_all_items
from settings.tokens import *

admin_blueprint = Blueprint("admin", __name__, template_folder="templates")

@admin_blueprint.route("/admin_dashboard")
def admin_dashboard():
    if USERNAME not in session:
        flash("Musisz być zalogowany, aby zobaczyć tę stronę.", "error")
        return redirect(url_for("auth.login"))
    if USERNAME in session and session.get(ADMIN):
        user_id = session[USER_ID]
        visible = is_visible(user_id)
        # users = get_all_users()  # Assuming this function returns a list of user objects
        users_data = get_all_users()
        items_data = get_all_items()
        return render_template("admin_dashboard.html", is_visible=visible, settings = load_settings(), available_spouses = get_available_spouses(), users_data = users_data, items_data = items_data, error_message = "")
    else:
        flash("Brak dostępu: musisz być administratorem.", "error")
        return redirect(url_for("auth.login"))
    


@admin_blueprint.route("/toggle_lottery", methods=["POST"])
def toggle_lottery():
    """Toggle the LOTTERY_ACTIVE setting."""
    print("Toggling lottery...")

    settings = load_settings()  # Load current settings
    settings["LOTTERY_ACTIVE"] = not settings["LOTTERY_ACTIVE"]  # Toggle the value
    save_settings(settings)  # Save updated settings

    return jsonify({"success": True, "LOTTERY_ACTIVE": settings["LOTTERY_ACTIVE"]})
