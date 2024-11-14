from flask import Flask
from config.settings import *  # Import necessary settings
from services.encryption_service import ensure_key_exists

# Ensure the encryption key exists at startup
ensure_key_exists()

# Initialize the app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set your secret key here

# Import blueprints
from routes.user_routes import user_blueprint
from routes.auth_routes import auth_blueprint
from routes.dashboard_routes import dashboard_blueprint
from routes.draw_routes import draw_blueprint
from routes.debug_routes import debug_blueprint

# Register blueprints
app.register_blueprint(user_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(dashboard_blueprint)
app.register_blueprint(draw_blueprint)
app.register_blueprint(debug_blueprint)

if __name__ == "__main__":
    
    app.run(debug=True)