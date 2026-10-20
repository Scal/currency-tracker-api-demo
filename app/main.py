from fastapi import FastAPI, HTTPException, Query


from app.schemas import (
    ConvertRequest,
    ConvertResponse,
    CurrencyCode,
    RateResponse,
)

from app.services import (
    convert_currency,
    get_latest_rates,
    get_rates_history,
)

app = FastAPI(title="Сервис мониторинга курса валют")

@app.get("/api/v1/rates/latest", response_model=list[RateResponse])
async def latest_rates():
    return await get_latest_rates()

@app.get("/api/v1/rates/history", response_model=list[RateResponse])
async def rates_history(
    currency: CurrencyCode,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return await get_rates_history(currency, limit, offset)

@app.post("/api/v1/convert", response_model=ConvertResponse)
async def convert(request: ConvertRequest):
    try:
        return await convert_currency(
            from_currency=request.from_currency,
            to_currency=request.to_currency,
            amount=request.amount,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        ) from error