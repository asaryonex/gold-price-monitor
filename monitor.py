import asyncio
import logging

from scraper import fetch_html, parse_prices
from database import (
    latest_price,
    insert_price,
    get_subscribers,
)

logger = logging.getLogger(__name__)


async def monitor_prices(application, interval):
    logger.info("Price monitor started")

    while True:
        try:
            current = parse_prices(fetch_html())
            previous = latest_price()

            # First run: save current prices without sending alerts
            if previous is None:
                save_price(
                    "Coimbatore",
                    current["24K"],
                    current["22K"],
                )
                logger.info("Initial prices saved: %s", current)

            elif current != previous:
                save_price(
                "Coimbatore",
                current["24K"],
                current["22K"],
                )
                message = (
                    "📢 Gold Price Updated\n\n"
                    f"24K : ₹{current['24K']:,}\n"
                    f"22K : ₹{current['22K']:,}"
                )

                for chat_id in get_subscribers():
                    try:
                        await application.bot.send_message(
                            chat_id=chat_id,
                            text=message,
                        )
                    except Exception as ex:
                        logger.exception(
                            "Failed to send message to %s: %s",
                            chat_id,
                            ex,
                        )

                logger.info("Price changed: %s", current)

            else:
                logger.info("No price change")

        except Exception:
            logger.exception("Error while checking prices")

        await asyncio.sleep(interval)