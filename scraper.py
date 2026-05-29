import requests
import json
from typing import TypedDict
import time
import csv


class TefasData(TypedDict):
    code: str
    description: str
    priceTRY: str
    changePercentageDaily: str
    changePercentage1Month: str
    changePercentage3Months: str
    changePercentage6Months: str
    changePercentage12Months: str


API_BASE = "https://www.tefas.gov.tr/api/funds"
AUTH_TOKEN = "Bearer ST-tefaswebwse3irfmSBj4iRAzGPbAlS94Se"

HEADERS = {
    "Authorization": AUTH_TOKEN,
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Origin": "https://www.tefas.gov.tr",
    "Referer": "https://www.tefas.gov.tr/tr/fon-detayli-analiz/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
}


INPUTS = [
    "TTA",
    "YKT",
    "GGK",
    "OTJ",
    "ZCN",
    "AES",
    "IIH",
    "TI2",
    "SAS",
    "YAS",
    "TI3",
    "IVY",
    "YTD",
    "YAY",
    "OJT",
    "DBH",
    "TI1",
    "AC4",
    "TZL",
]


def format_number(value: "float | None") -> "str | None":
    if value is None:
        return None
    return f"{value:.6f}".rstrip("0").rstrip(".")


def fetch_period_return(session: requests.Session, fund_code: str, period: int) -> "float | None":
    resp = session.post(
        f"{API_BASE}/fonProfilDtyGetir",
        headers=HEADERS,
        data=json.dumps({"dil": "TR", "fonKodu": fund_code, "periyod": str(period)}),
        timeout=30,
    )
    resp.raise_for_status()
    payload = resp.json()
    for row in payload.get("resultList") or []:
        if row.get("fonKodu") == fund_code:
            ret = row.get("fonTurGetiri")
            return ret * 100 if ret is not None else None
    return None


def fetch_price_history(session: requests.Session, fund_code: str) -> list:
    resp = session.post(
        f"{API_BASE}/fonFiyatBilgiGetir",
        headers=HEADERS,
        data=json.dumps({"fonKodu": fund_code, "dil": "TR", "periyod": 12}),
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json().get("resultList") or []


def fetch_fund_data(session: requests.Session, fund_code: str) -> TefasData:
    history = fetch_price_history(session, fund_code)
    history.sort(key=lambda r: r["tarih"])

    description = history[-1]["fonUnvan"] if history else None
    last_price = history[-1]["fiyat"] if history else None
    daily_change = None
    if len(history) >= 2 and history[-2]["fiyat"]:
        prev = history[-2]["fiyat"]
        daily_change = (last_price - prev) / prev * 100

    return {
        "code": fund_code,
        "description": description,
        "priceTRY": format_number(last_price),
        "changePercentageDaily": format_number(daily_change),
        "changePercentage1Month": format_number(fetch_period_return(session, fund_code, 1)),
        "changePercentage3Months": format_number(fetch_period_return(session, fund_code, 3)),
        "changePercentage6Months": format_number(fetch_period_return(session, fund_code, 6)),
        "changePercentage12Months": format_number(fetch_period_return(session, fund_code, 12)),
    }


def update_funds():
    session = requests.Session()
    fund_data = []
    for code in INPUTS:
        data = fetch_fund_data(session, code)
        fund_data.append(data)
        time.sleep(0.50)

    with open("fund_data.json", "w", encoding="utf-8") as json_file:
        json.dump(fund_data, json_file, indent=4, ensure_ascii=False)

    with open("fund_data.csv", "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fund_data[0].keys())
        writer.writeheader()
        for fund in fund_data:
            writer.writerow(fund)

    print("Data written to fund_data.json and fund_data.csv files.")


update_funds()
