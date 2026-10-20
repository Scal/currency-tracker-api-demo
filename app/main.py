from fastapi import FastAPI, Query
from typing import Literal

from app.schemas import RateResponse
from app.services import get_latest_rates, get_rates_history

app = FastAPI(title="Сервис мониторинга курса валют")


@app.get("/api/v1/rates/latest", response_model=list[RateResponse])
async def latest_rates():
    return await get_latest_rates()

@app.get("/api/v1/rates/history", response_model=list[RateResponse])
async def rates_history(
    currency: Literal["USD", "EUR", "CNY"],
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return await get_rates_history(currency, limit, offset)