from flask import Blueprint, render_template, session, redirect, url_for, flash, jsonify, request
from services.verification import is_visible
from settings.settings import load_settings, save_settings
from services.lists_service import get_available_spouses, get_all_users, get_all_items
from settings.tokens import *

admin_blueprint = Blueprint("admin", __name__, template_folder="templates")

@admin_blueprint.route("/admin_dashboard")
def admin_dashboard():
    if "username" in session and session.get("is_admin"):
        user_id = session["user_id"]
        visible = is_visible(user_id)
        # users = get_all_users()  # Assuming this function returns a list of user objects
        users_data = get_all_users()
        items_data = get_all_items()
        return render_template("admin_dashboard.html", is_visible=visible, settings = load_settings(), available_spouses = get_available_spouses(), users_data = users_data, items_data = items_data)
    else:
        flash("Brak dostępu: musisz być administratorem.", "error")
        return redirect(url_for("auth.login"))
    
@admin_blueprint.route("/admin.update_user")
def update_user() :
    print("updating")
    pass


@admin_blueprint.route("/admin/toggle_lottery", methods=["POST"])
def toggle_lottery():
    print("Toggling lottery...")

    settings = load_settings()  # Load current settings
    settings["LOTTERY_ACTIVE"] = not settings["LOTTERY_ACTIVE"]  # Toggle the value
    save_settings(settings)  # Save updated settings

    return jsonify({"success": True, "LOTTERY_ACTIVE": settings["LOTTERY_ACTIVE"]})


@admin_blueprint.route("/admin.unreserve_wishlist_item")
def unreserve_wishlist_item() :
    print("unreserving")
    pass

@admin_blueprint.route("/admin.edit_wishlist_item")
def edit_wishlist_item() :
    print("editing")
    pass

@admin_blueprint.route("/admin.remove_wishlist_item")
def remove_wishlist_item() :
    print("removing")
    pass

