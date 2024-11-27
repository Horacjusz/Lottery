from flask import session, flash, redirect, url_for, render_template, Blueprint
from services.file_service import load_settings
from services.file_service import load_user_data
from services.lists_service import get_all_items, get_all_users
from settings.tokens import *


dashboard_blueprint = Blueprint("dashboard", __name__)

@dashboard_blueprint.route("/dashboard")
def dashboard():
    if USERNAME not in session:
        flash("Musisz być zalogowany, aby zobaczyć tę stronę.", "error")
        return redirect(url_for("auth.login"))

    user_id = session[USER_ID]
    user_data = load_user_data(user_id)

    if user_data is None:
        flash("Nie znaleziono danych użytkownika. Proszę spróbować ponownie.", "error")
        return redirect(url_for("auth.logout"))
    
    items = get_all_items()
    
    for item in items : 
        print(items[item])

    return render_template("dashboard.html", 
                           user = user_data, 
                           settings = load_settings(), 
                           items_data = get_all_items(), 
                           users_data = get_all_users())
