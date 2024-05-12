import requests
from bs4 import BeautifulSoup
import json
from typing import TypedDict
import time
import csv


class TefasData(TypedDict):
    code: str
    price: float
    description: str
    dailyChange: str


class CssSelectors:
    PRICE = "#MainContent_PanelInfo > div.main-indicators > ul.top-list > li:nth-child(1) > span"
    DESCRIPTION = "#MainContent_PanelInfo > div:nth-of-type(1) > h2"
    CHANGE_DAILY = "#MainContent_PanelInfo > div.main-indicators > ul.top-list > li:nth-child(2) > span"
    CHANGE_1_MONTH = (
        "#MainContent_PanelInfo > div.price-indicators > ul > li:nth-child(1) > span"
    )
    CHANGE_3_MONTH = (
        "#MainContent_PanelInfo > div.price-indicators > ul > li:nth-child(2) > span"
    )
    CHANGE_6_MONTH = (
        "#MainContent_PanelInfo > div.price-indicators > ul > li:nth-child(3) > span"
    )
    CHANGE_12_MONTH = (
        "#MainContent_PanelInfo > div.price-indicators > ul > li:nth-child(4) > span"
    )


INPUTS = [
    "TTA",
    "YKT",
    "GGK",
    "OTJ",
    "ZCN",
    "AES",
    "IIH",
    "SAS",
    "YAS",
    "TI3",
    "IVY",
    "YTD",
    "YAY",
    "OJT",
    "DBH",
    "TI1",
]


def parse_value(soup: BeautifulSoup, selector: str) -> "str | None":
    element = soup.select_one(selector).text
    if element:
        return element.strip().replace("%", "").replace(",", ".")
    else:
        return None


def fetch_fund_data(fund_code: str) -> TefasData:
    url = f"https://www.tefas.gov.tr/FonAnaliz.aspx?FonKod={fund_code}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser", from_encoding="utf-8")

    return {
        "code": fund_code,
        "description": parse_value(soup, CssSelectors.DESCRIPTION),
        "priceTRY": parse_value(soup, selector=CssSelectors.PRICE),
        "changePercentageDaily": parse_value(soup, CssSelectors.CHANGE_DAILY),
        "changePercentage1Month": parse_value(soup, CssSelectors.CHANGE_1_MONTH),
        "changePercentage3Month": parse_value(soup, CssSelectors.CHANGE_3_MONTH),
        "changePercentage6Month": parse_value(soup, CssSelectors.CHANGE_6_MONTH),
        "changePercentage9Month": parse_value(soup, CssSelectors.CHANGE_12_MONTH),
    }


def update_funds():
    fund_data = []
    for code in INPUTS:
        data = fetch_fund_data(code)
        fund_data.append(data)
        time.sleep(0.50)

    # Write to JSON file
    with open("fund_data.json", "w", encoding="utf-8") as json_file:
        json.dump(fund_data, json_file, indent=4, ensure_ascii=False)

    # Write to CSV file
    with open("fund_data.csv", "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fund_data[0].keys())
        writer.writeheader()
        for fund in fund_data:
            writer.writerow(fund)

    print("Data written to fund_data.json and fund_data.csv files.")


update_funds()
