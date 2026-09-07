from datetime import datetime, timezone
from flask import Blueprint, jsonify
from sqlalchemy import text
from ...database.base import engine
from ...config import get_settings

health_bp = Blueprint("health", __name__)
settings = get_settings()


@health_bp.route("/health", methods=["GET"])
def get_health():
    """System health check and diagnostic endpoint."""
    services = {
        "database": "unknown",
        "redis": "configured"
    }

    # Verify Database connectivity
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            services["database"] = "connected"
    except Exception as e:
        services["database"] = f"unhealthy: {str(e)}"

    overall_status = "healthy" if services["database"] == "connected" else "degraded"

    return jsonify({
        "status": overall_status,
        "platform": "ResearchOS",
        "version": "1.0.0",
        "environment": settings.FLASK_ENV,
        "services": services,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200
