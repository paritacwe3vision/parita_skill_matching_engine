import os

from dotenv import load_dotenv
from supabase import create_client

# ---------------------------------------------------
# Current directory
# database/
# ---------------------------------------------------

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------
# Project Root
# ---------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        CURRENT_DIR,
        ".."
    )
)

# ---------------------------------------------------
# .env file (project root)
# ---------------------------------------------------

ENV_PATH = os.path.join(
    PROJECT_ROOT,
    ".env"
)

print("ENV_PATH:", ENV_PATH)
print("Exists:", os.path.exists(ENV_PATH))

load_dotenv(ENV_PATH)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("SUPABASE_URL:", SUPABASE_URL)

if not SUPABASE_URL:
    raise Exception("SUPABASE_URL not found.")

if not SUPABASE_KEY:
    raise Exception("SUPABASE_KEY not found.")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)