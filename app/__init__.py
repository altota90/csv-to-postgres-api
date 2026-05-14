from flask import Flask
from app.routes import routes
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    # Enable CORS so React can call the API
    CORS(app)

    # Register Blueprint
    app.register_blueprint(routes)
    
    return app