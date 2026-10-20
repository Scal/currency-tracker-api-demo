from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class RateResponse(BaseModel):
    id: int
    currency_code: str
    rate: Decimal
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)