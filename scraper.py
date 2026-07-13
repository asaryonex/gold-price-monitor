import re
import httpx
from bs4 import BeautifulSoup
from config import GOODRETURNS_URL
import logging

logger = logging.getLogger(__name__)

def fetch_html():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "AppleWebKit/537.36 "
            "Chrome/138.0 Safari/537.36"
        )
    }

    response = httpx.get(
        GOODRETURNS_URL,
        headers=headers,
        timeout=30,
        follow_redirects=True,
    )

    response.raise_for_status()

    return response.text


import re
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def parse_prices(html: str):
    soup = BeautifulSoup(html, "lxml")

    table = soup.find("table")
    if table is None:
        raise Exception("Price table not found.")

    for row in table.find_all("tr"):
        cols = [td.get_text(" ", strip=True) for td in row.find_all(["td", "th"])]

        if not cols:
            continue

        if cols[0] == "1":
            logger.info("cols = %s", cols)

            # Extract the first ₹ amount only
            m24 = re.search(r"₹\s*([\d,]+)", cols[1])
            m22 = re.search(r"₹\s*([\d,]+)", cols[2])

            if not m24 or not m22:
                raise Exception(f"Unable to parse prices: {cols}")

            return {
                "24K": int(m24.group(1).replace(",", "")),
                "22K": int(m22.group(1).replace(",", "")),
            }

    raise Exception("Unable to locate 1 gram row.")


if __name__ == "__main__":

    html = fetch_html()

    prices = parse_prices(html)

    logger.info("\nToday's Coimbatore Gold Price\n")
    logger.info(prices)