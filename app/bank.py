from decimal import Decimal
from xml.etree import ElementTree

import httpx


CBR_URL = "https://www.cbr.ru/scripts/XML_daily.asp"
SUPPORTED_CURRENCIES = {"USD", "EUR", "CNY"}

async def fetch_rates_xml() -> bytes:
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(CBR_URL)
        response.raise_for_status()
        return response.content


def parse_rates_xml(xml_data: bytes) -> dict[str, Decimal]:
    root = ElementTree.fromstring(xml_data)
    rates = {}

    for currency in root.findall("Valute"):
        code = currency.findtext("CharCode")

        if code not in SUPPORTED_CURRENCIES:
            continue

        value_text = currency.findtext("Value")
        nominal_text = currency.findtext("Nominal")

        if value_text is None or nominal_text is None:
            raise ValueError(f"Неполные данные курса {code}")

        value = Decimal(value_text.replace(",", "."))
        nominal = Decimal(nominal_text)

        if not value.is_finite() or not nominal.is_finite():
            raise ValueError(f"Некорректный курс {code}")

        if value <= 0 or nominal <= 0:
            raise ValueError(f"Курс и номинал {code} должны быть положительными")

        rates[code] = value / nominal

    if rates.keys() != SUPPORTED_CURRENCIES:
        raise ValueError("В ответе ЦБ отсутствуют необходимые валюты")

    return rates

async def fetch_rates() -> dict[str, Decimal]:
    xml_data = await fetch_rates_xml()
    return parse_rates_xml(xml_data)