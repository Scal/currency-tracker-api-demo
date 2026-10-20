from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

CurrencyCode = Literal["RUB", "USD", "EUR", "CNY"]

class RateResponse(BaseModel):
    id: int
    currency_code: str
    rate: Decimal
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ConvertRequest(BaseModel):
    from_currency: CurrencyCode
    to_currency: CurrencyCode
    amount: Decimal = Field(ge=0, allow_inf_nan=False)

class ConvertResponse(BaseModel):
    result: float
    rate_used: float