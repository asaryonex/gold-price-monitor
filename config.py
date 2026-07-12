import os
from dotenv import load_dotenv

load_dotenv()

print("BOT_TOKEN:", os.getenv("BOT_TOKEN"))
print("CHECK_INTERVAL:", os.getenv("CHECK_INTERVAL"))
print("GOODRETURNS_URL:", os.getenv("GOODRETURNS_URL"))

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing.")

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "300"))
GOODRETURNS_URL = os.getenv(
    "GOODRETURNS_URL",
    "https://www.goodreturns.in/gold-rates/coimbatore.html",
)