import os
from flask import Flask, jsonify
from flask_cors import CORS
from .config import get_settings
from .database.base import init_db
from .api.routes.health import health_bp
from .api.routes.research import research_bp
from .utils import logger


def create_app(config_override: dict = None) -> Flask:
    """Flask Application Factory."""
    app = Flask(__name__)
    settings = get_settings()

    # Configuration
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["ENV"] = settings.FLASK_ENV
    app.config["DEBUG"] = settings.FLASK_DEBUG

    if config_override:
        app.config.update(config_override)

    # Enable CORS for frontend integration
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize Database Tables
    try:
        init_db()
    except Exception as e:
        logger.error(f"Database initialization warning: {e}")

    # Register Blueprints
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(research_bp, url_prefix="/api")

    # Global Error Handlers
    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({"error": "Resource not found", "status_code": 404}), 404

    @app.errorhandler(500)
    def handle_500(e):
        return jsonify({"error": "Internal server error", "status_code": 500}), 500

    logger.info("ResearchOS Flask Application initialized successfully.")
    return app
