import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Database settings
DB_TYPE = os.getenv("DB_TYPE", "sqlite")
DB_NAME = os.getenv("DB_NAME", "taco_quest.db")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "")
DB_PORT = os.getenv("DB_PORT", "")

# Supabase settings
USE_SUPABASE = os.getenv("USE_SUPABASE", "False").lower() in ("true", "1", "t")
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
SUPABASE_PUBLIC_KEY = os.getenv("SUPABASE_PUBLIC_KEY", "")

# Supabase direct database connection (optional)
SUPABASE_DB_HOST = os.getenv("SUPABASE_DB_HOST", "")
SUPABASE_DB_PORT = os.getenv("SUPABASE_DB_PORT", "5432")
SUPABASE_DB_NAME = os.getenv("SUPABASE_DB_NAME", "postgres")
SUPABASE_DB_USER = os.getenv("SUPABASE_DB_USER", "postgres")
SUPABASE_DB_PASSWORD = os.getenv("SUPABASE_DB_PASSWORD", "")

# Construct database URL based on type
if DB_TYPE == "sqlite":
    DATABASE_URL = f"sqlite:///{BASE_DIR}/{DB_NAME}"
elif DB_TYPE == "postgresql":
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
elif DB_TYPE == "supabase" or USE_SUPABASE:
    # For direct PostgreSQL connection to Supabase
    DATABASE_URL = f"postgresql://{SUPABASE_DB_USER}:{SUPABASE_DB_PASSWORD}@{SUPABASE_DB_HOST}:{SUPABASE_DB_PORT}/{SUPABASE_DB_NAME}"
else:
    # Default to SQLite
    DATABASE_URL = f"sqlite:///{BASE_DIR}/{DB_NAME}"

# Application settings
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")
ECHO_SQL = os.getenv("ECHO_SQL", "False").lower() in ("true", "1", "t")

# API settings
API_VERSION = os.getenv("API_VERSION", "v1")
API_PREFIX = f"/api/{API_VERSION}"
