import re
import httpx
from bs4 import BeautifulSoup
from config import GOODRETURNS_URL


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


def parse_prices(html: str):
    soup = BeautifulSoup(html, "lxml")

    table = soup.find("table")

    if table is None:
        raise Exception("Price table not found.")

    rows = table.find_all("tr")

    for row in rows:

        cols = [
            td.get_text(" ", strip=True)
            for td in row.find_all(["td", "th"])
        ]

        if not cols:
            continue

        # First row containing 1 Gram price
        if cols[0] == "1":

            price24 = int(re.sub(r"[^\d]", "", cols[1]))
            price22 = int(re.sub(r"[^\d]", "", cols[2]))

            return {
                "24K": price24,
                "22K": price22,
            }

    raise Exception("Unable to locate 1 gram row.")


if __name__ == "__main__":

    html = fetch_html()

    prices = parse_prices(html)

    print("\nToday's Coimbatore Gold Price\n")
    print(prices)