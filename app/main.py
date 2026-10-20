from fastapi import FastAPI

from app.schemas import RateResponse
from app.services import get_latest_rates


app = FastAPI(title="Сервис мониторинга курса валют")


@app.get("/api/v1/rates/latest", response_model=list[RateResponse])
async def latest_rates():
    return await get_latest_rates()