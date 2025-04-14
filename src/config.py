import os
from dotenv import load_dotenv


dirname = os.path.dirname(__file__)
load_dotenv(dotenv_path=os.path.join(dirname, "..", ".env"))

DATABASE_PATH = os.getenv("DATABASE_PATH") or "./data/default.db"
USER_AGENT = os.getenv("USER_AGENT") or "MagicArchive"
