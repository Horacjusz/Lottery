from flask import Blueprint, render_template, session, redirect, url_for, flash, jsonify
from services.verification import is_visible
from services.file_service import load_settings, save_settings
from services.lists_service import get_all_users, get_all_items
from services.draw_service import reset_draw
from sqlalchemy import text
from services.database import datasession
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
        users_data = get_all_users()
        items_data = get_all_items()
        return render_template("admin_dashboard.html", is_visible=visible, settings = load_settings(), users_data = users_data, items_data = items_data, error_message = "", admin_id = user_id)
    else:
        flash("Brak dostępu: musisz być administratorem.", "error")
        return redirect(url_for("auth.login"))

@admin_blueprint.route("/toggle_lottery", methods=["POST"])
def toggle_lottery():
    settings = load_settings()
    settings["LOTTERY_ACTIVE"] = not settings["LOTTERY_ACTIVE"]
    save_settings(settings)

    return jsonify({"success": True, "LOTTERY_ACTIVE": settings["LOTTERY_ACTIVE"]})

@admin_blueprint.route("/reset_lottery", methods=["POST"])
def reset_lottery():
    reset_draw()
    return jsonify({"success": True})

def truncate_tables():
    try:
        datasession.execute(text("TRUNCATE TABLE items CASCADE"))
        datasession.execute(text("TRUNCATE TABLE users CASCADE"))
        datasession.commit()
        print("All tables truncated successfully.")
    except Exception as e:
        datasession.rollback()
        print(f"Error truncating tables: {e}")
