import requests
from bs4 import BeautifulSoup
import json
from typing import TypedDict
import time


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


INPUTS = ["YAS", "TTE"]


def parse_value(soup: BeautifulSoup, selector: str) -> str | None:
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
        fund_data.append(fetch_fund_data(code))
        time.sleep(0.150)

    print(json.dumps(fund_data, indent=4, ensure_ascii=False))
    with open("fund_data.json", "w", encoding="utf-8") as f:
        json.dump(fund_data, f, indent=4, ensure_ascii=False)


update_funds()
