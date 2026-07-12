import asyncio

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from config import BOT_TOKEN, CHECK_INTERVAL
from scraper import fetch_html, parse_prices
from storage import (
    subscribe,
    unsubscribe,
    load_subscribers,
)
from monitor import monitor_prices


# -----------------------------
# Commands
# -----------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "👋 Welcome to Gold Price Monitor Bot!\n\n"
        "Available Commands:\n\n"
        "/price - Current Coimbatore Gold Price\n"
        "/subscribe - Receive automatic alerts\n"
        "/unsubscribe - Stop receiving alerts\n"
        "/subscribers - View subscriber count"
    )

    await update.message.reply_text(message)


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        html = fetch_html()
        prices = parse_prices(html)

        message = (
            "📈 Today's Coimbatore Gold Price\n\n"
            f"24K : ₹{prices['24K']:,}\n"
            f"22K : ₹{prices['22K']:,}"
        )

        await update.message.reply_text(message)

    except Exception as e:
        await update.message.reply_text(f"❌ Error\n\n{e}")


async def subscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    subscribe(chat_id)

    await update.message.reply_text(
        "✅ Successfully subscribed!\n\n"
        "You'll now receive automatic gold price alerts."
    )


async def unsubscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    unsubscribe(chat_id)

    await update.message.reply_text(
        "❌ You have been unsubscribed."
    )


async def subscribers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    count = len(load_subscribers())

    await update.message.reply_text(
        f"👥 Total Subscribers: {count}"
    )


# -----------------------------
# Background Monitor
# -----------------------------

async def post_init(application: Application):
    asyncio.create_task(
        monitor_prices(application, CHECK_INTERVAL)
    )


# -----------------------------
# Main
# -----------------------------

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.post_init = post_init

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("subscribe", subscribe_command))
    app.add_handler(CommandHandler("unsubscribe", unsubscribe_command))
    app.add_handler(CommandHandler("subscribers", subscribers))

    print("=" * 50)
    print("Gold Price Monitor Bot Started")
    print("=" * 50)

    app.run_polling()


if __name__ == "__main__":
    main()