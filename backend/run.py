import os
from app import create_app
from app.config import get_settings
from app.utils import logger

settings = get_settings()
app = create_app()

if __name__ == "__main__":
    logger.info(f"Starting ResearchOS API Server on {settings.HOST}:{settings.PORT} (debug={settings.FLASK_DEBUG})")
    app.run(
        host=settings.HOST,
        port=settings.PORT,
        debug=settings.FLASK_DEBUG,
        threaded=True
    )
