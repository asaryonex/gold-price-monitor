import json
from pathlib import Path

PRICE_FILE = Path("prices.json")
SUBSCRIBER_FILE = Path("subscribers.json")


# ---------- Price Storage ----------

def load_prices():
    if not PRICE_FILE.exists():
        return None

    with open(PRICE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_prices(prices):
    with open(PRICE_FILE, "w", encoding="utf-8") as f:
        json.dump(prices, f, indent=2)


# ---------- Subscribers ----------

def load_subscribers():
    if not SUBSCRIBER_FILE.exists():
        return []

    with open(SUBSCRIBER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_subscribers(subscribers):
    with open(SUBSCRIBER_FILE, "w", encoding="utf-8") as f:
        json.dump(subscribers, f, indent=2)


def subscribe(chat_id: int):
    subscribers = load_subscribers()

    if chat_id not in subscribers:
        subscribers.append(chat_id)
        save_subscribers(subscribers)

    return subscribers


def unsubscribe(chat_id: int):
    subscribers = load_subscribers()

    if chat_id in subscribers:
        subscribers.remove(chat_id)
        save_subscribers(subscribers)

    return subscribers