import os
from dotenv import load_dotenv

# Load local .env variables
load_dotenv()


class Config:
    """
    Application configuration values.
    """

    # Flask Settings
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "cybersecurity-passhashpie-secret-key-3f363eb4"
    )
    DEBUG = os.environ.get("FLASK_DEBUG", "True").lower() == "true"

    # HaveIBeenPwned API Settings
    HIBP_API_URL = "https://api.pwnedpasswords.com/range"

    # Optional Gemini AI Settings
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

    # Path settings
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATASETS_DIR = os.path.join(BASE_DIR, "datasets")
