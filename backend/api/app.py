"""Flask application factory"""
from flask import Flask
from flask_cors import CORS
from .routes import register_routes


def create_app():
    """Create and configure Flask app"""
    app = Flask(__name__)
    CORS(app)
    
    # Register routes
    register_routes(app)
    
    return app


app = create_app()
