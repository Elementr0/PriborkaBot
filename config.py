import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN=os.getenv("BOT_TOKEN")
ADMIN=os.getenv("ADMIN").split(",") if os.getenv("ADMIN") else []
DATABASE_URL=os.getenv("DATABASE_URL")