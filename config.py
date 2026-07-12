from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "600"))
GOODRETURNS_URL = os.getenv(
    "GOODRETURNS_URL",
    "https://www.goodreturns.in/gold-rates/coimbatore.html",
)