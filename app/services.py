from datetime import datetime, timezone
from app.bank import fetch_rates
from app.db import session_factory
from app.models import CurrencyRate
from sqlalchemy import select
from decimal import Decimal, ROUND_HALF_UP


async def update_rates() -> int:
    rates = await fetch_rates()
    received_at = datetime.now(timezone.utc)

    records = [
        CurrencyRate(
            currency_code=code,
            rate=rate,
            updated_at=received_at,
        )
        for code, rate in rates.items()
    ]

    async with session_factory.begin() as session:
        session.add_all(records)

    return len(records)


async def get_latest_rates() -> list[CurrencyRate]:
    statement = (
        select(CurrencyRate)
        .distinct(CurrencyRate.currency_code)
        .order_by(
            CurrencyRate.currency_code,
            CurrencyRate.updated_at.desc(),
            CurrencyRate.id.desc(),
        )
    )

    async with session_factory() as session:
        result = await session.scalars(statement)
        return list(result.all())


async def get_rates_history(
    currency: str,
    limit: int,
    offset: int,
) -> list[CurrencyRate]:
    statement = (
        select(CurrencyRate)
        .where(CurrencyRate.currency_code == currency)
        .order_by(
            CurrencyRate.updated_at.desc(),
            CurrencyRate.id.desc(),
        )
        .limit(limit)
        .offset(offset)
    )

    async with session_factory() as session:
        result = await session.scalars(statement)
        return list(result.all())


async def convert_currency(
    from_currency: str,
    to_currency: str,
    amount: Decimal,
) -> dict[str, Decimal]:
    if from_currency == to_currency:
        rate_used = Decimal("1")
    else:
        records = await get_latest_rates()
        rates = {record.currency_code: record.rate for record in records}
        rates["RUB"] = Decimal("1")

        if from_currency not in rates or to_currency not in rates:
            raise ValueError("Необходимые курсы ещё не загружены")

        rate_used = rates[from_currency] / rates[to_currency]

    result = (amount * rate_used).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    return {
        "result": result,
        "rate_used": rate_used,
    }