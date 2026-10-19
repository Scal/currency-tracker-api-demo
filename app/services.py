from datetime import datetime, timezone

from app.bank import fetch_rates
from app.db import session_factory
from app.models import CurrencyRate


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