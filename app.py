from flask import Flask, redirect, url_for, session
from datetime import timedelta
from settings.settings import *
from generation.generate_owner import generate_owner
import os

from routes.auth_routes import auth_blueprint
from routes.dashboard_routes import dashboard_blueprint
from routes.draw_routes import draw_blueprint
from routes.admin_routes import admin_blueprint
from routes.item_routes import item_blueprint
from routes.user_routes import user_blueprint



app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'  # Set your secret key here

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


if __name__ == "__main__":
    
    generate_owner()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    # app.run(debug=True)