from flask import Flask
import os
from flask_cors import CORS
from routes import register_routes
from auth import DATA_FILE

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.secret_key = os.urandom(24)

    # Create data file if it doesn't exist
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            pass

    # Register all routes
    register_routes(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 