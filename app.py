import gunicorn
from flask import Flask, redirect, url_for, session
from datetime import timedelta
from settings.settings import *
from generation.generate_owner import generate_owner
import os
from services.database import initialize_db
from settings.settings import DEFAULT_SETTINGS
from services.file_service import save_settings
from dotenv import load_dotenv

from routes.auth_routes import auth_blueprint
from routes.dashboard_routes import dashboard_blueprint
from routes.draw_routes import draw_blueprint
from routes.admin_routes import admin_blueprint
from routes.item_routes import item_blueprint
from routes.user_routes import user_blueprint

load_dotenv()


app = Flask(__name__, static_folder='static')
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")

app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes = 5)
app.config["SESSION_PERMANENT"] = True

app.register_blueprint(item_blueprint, url_prefix="/items")
app.register_blueprint(auth_blueprint)
app.register_blueprint(dashboard_blueprint)
app.register_blueprint(draw_blueprint, url_prefix="/draw")
app.register_blueprint(admin_blueprint, url_prefix="/admin")
app.register_blueprint(user_blueprint, url_prefix="/users")



@app.route("/")
def home():
    return redirect(url_for("auth.login"))

@app.before_request
def refresh_session():
    session.modified = True

def prepare_app() :
    initialize_db()
    save_settings(DEFAULT_SETTINGS)
    generate_owner()
    

if __name__ == "__main__":
    prepare_app()
    port = int(os.getenv("PORT", 5000))
    app.run(debug=os.getenv("FLASK_ENV") == "development", port=port)
