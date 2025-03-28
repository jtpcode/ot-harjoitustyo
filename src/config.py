import os
from dotenv import load_dotenv

dirname = os.path.dirname(__file__)

try:
    load_dotenv(dotenv_path=os.path.join(dirname, "..", ".env"))
except FileNotFoundError:
    print("File .env not found.")

DATABASE_PATH = os.getenv("DATABASE_PATH") or "default.db"
