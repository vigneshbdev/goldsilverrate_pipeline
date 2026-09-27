import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
from src.models.gold_silver_rate import RateDiff, GoldSilverRate

URL = "https://www.livechennai.com/gold_silverrate.asp"

def fetch_page() -> str :

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/140.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(
        URL,
        headers=headers,
        timeout=15,
    )

    response.raise_for_status()

    return response.text

def clean_rate(value: str) -> str:
    return value.replace(",","").strip()

def get_rate(value: str) -> float:
    return float(value.split("(")[0].strip())

def get_diff(value: str) -> float:
    parts = value.split("(")
    return float(parts[1].replace(")", "").strip()) if len(parts) > 1 else 0

def extract_rates(str) -> RateDiff:
    return RateDiff(
        diff=get_diff(clean_rate(str)),
        rate=get_rate(clean_rate(str))
    )

def scrape_rates() -> GoldSilverRate:
    html = fetch_page()

    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table")
    table_0 = tables[0]
    cells = [
        cell.get_text(" ", strip=True)
        for cell in table_0.find_all(["th", "td"])
    ]

    table_1 = tables[1]

    # The 24K historical table contains the current and previous
    # day's rates, but does not provide the daily difference.
    # Read the date and 24K rate from the table and calculate the
    # difference ourselves.
    rows = table_1.find_all("tr")

    rate_rows = []

    for row in rows:
        row_cells = [
            cell.get_text(" ", strip=True)
            for cell in row.find_all(["th", "td"])
        ]

        if len(row_cells) < 2:
            continue

        date_text = row_cells[0].strip()
        rate_text = clean_rate(row_cells[1])

        try:
            rate = get_rate(rate_text)
        except (ValueError, IndexError):
            continue

        if not date_text or rate <= 0:
            continue

        parsed_date = None
        for fmt in (
            "%d/%b/%Y",
            "%d/%B/%Y",
            "%d/%m/%Y",
            "%d-%m-%Y",
            "%d/%b/%y",
            "%d-%b-%y",
        ):
            try:
                parsed_date = datetime.strptime(date_text, fmt).date()
                break
            except ValueError:
                pass

        if parsed_date is not None:
            rate_rows.append((parsed_date, rate))

    rate_rows.sort(key=lambda item: item[0], reverse=True)

    if len(rate_rows) < 2:
        raise ValueError(
            "Unable to find today's and previous day's 24K gold rates."
        )

    today_24k_date, today_24k_rate = rate_rows[0]
    previous_24k_date, previous_24k_rate = rate_rows[1]

    gold_24k = RateDiff(
        rate=today_24k_rate,
        diff=today_24k_rate - previous_24k_rate,
    )

    gold_22k = extract_rates(cells[4])
    silver = extract_rates(cells[5])

    return GoldSilverRate(
        date=date.today(),
        gold22KRate=gold_22k,
        gold24KRate=gold_24k,
        silverRate=silver
    )


def main():
    rates = scrape_rates()
    print(f"Today's rates {rates}")

if __name__ == "__main__":
    main()