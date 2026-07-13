import asyncio
import logging

from telegram.error import BadRequest, Forbidden, TelegramError
from scraper import fetch_html, parse_prices
from database import (
    latest_price,
    insert_price,
    get_subscribers,
    unsubscribe,
)

logger = logging.getLogger(__name__)


async def monitor_prices(application, interval):
    logger.info("Price monitor started")

    while True:
        try:
            current = parse_prices(fetch_html())
            previous = latest_price()

            logger.info("Previous: %s", previous)
            logger.info("Current : %s", current)

            # First run: save current prices without sending alerts
            if previous is None:
                insert_price(
                    "Coimbatore",
                    current["24K"],
                    current["22K"],
                )
                logger.info("Initial prices saved: %s", current)

            elif current != previous:
                insert_price(
                    "Coimbatore",
                    current["24K"],
                    current["22K"],
                )
                message = (
                    "📢 Gold Price Updated\n\n"
                    f"24K : ₹{current['24K']:,}\n"
                    f"22K : ₹{current['22K']:,}"
                )

                subscribers = get_subscribers()
                logger.info("Subscribers: %s", subscribers)

                for chat_id in subscribers:
                    try:
                        await application.bot.send_message(
                            chat_id=chat_id,
                            text=message,
                        )

                        logger.info("✅ Sent to %s", chat_id)

                    except (BadRequest, Forbidden) as ex:
                        logger.warning(
                            "Removing invalid subscriber %s (%s)",
                            chat_id,
                            ex,
                        )
                        unsubscribe(chat_id)

                    except TelegramError as ex:
                        logger.warning(
                            "Telegram error for %s: %s",
                            chat_id,
                            ex,
                        )

                    except Exception:
                        logger.exception(
                            "Unexpected error while sending to %s",
                            chat_id,
                        )

                logger.info("Price changed: %s", current)

        except Exception:
            logger.exception("Error while monitoring prices")

        await asyncio.sleep(interval)
