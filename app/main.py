from fastapi import FastAPI
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file at the very start
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Print to verify that the variable is being loaded
# print("GEMINI_API_KEY from dotenv:", os.getenv("GEMINI_API_KEY"))

from app.middlewares.file_validation import FileValidationMiddleware
from app.middlewares.rate_limit import RateLimitMiddleware
from app.routers.file_router import router
from app.config.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if not settings.gemini_config.API_KEY:
    logger.warning("GEMINI_API_KEY is not set. Some features may not work properly.")

# Log environment variables (excluding sensitive data)
logger.info(f"UPLOAD_FOLDER set to: {settings.UPLOAD_FOLDER}")
logger.info(f"GEMINI_API_KEY is {'set' if settings.gemini_config.API_KEY else 'not set'}")

app = FastAPI(redirect_slashes=False)

# Create upload directory if it doesn't exist
# If cannot create directory, raise an exception
try:
    if not os.path.exists(settings.UPLOAD_FOLDER):
        os.makedirs(settings.UPLOAD_FOLDER)
except Exception as e:
    logger.error(f"Failed to create upload folder: {e}")
    raise

app.add_middleware(FileValidationMiddleware)
app.add_middleware(RateLimitMiddleware)

app.include_router(router)
