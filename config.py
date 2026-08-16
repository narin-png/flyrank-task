from dotenv import load_dotenv
from sqlmodel import create_engine
import os

# Load variables from .env file into environment
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Did you create a .env file in the project root?"
    )

# Single shared engine used across the whole app
engine = create_engine(DATABASE_URL, echo=False)