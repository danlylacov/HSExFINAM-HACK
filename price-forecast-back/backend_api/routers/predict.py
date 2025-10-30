from fastapi import APIRouter, HTTPException
from backend_api.models.schemas import PredictionRequest, MultiTickerReturnsResponse
from backend_api.services.model_service import ensemble_models
from backend_api.services.prediction_service import process_multiple_tickers

router = APIRouter()

@router.post("/predict", response_model=MultiTickerReturnsResponse)
async def predict_returns(request: PredictionRequest):
    if not ensemble_models:
        raise HTTPException(status_code=503, detail="Модели не загружены")
    if not request.params:
        raise HTTPException(status_code=400, detail="Пустой список параметров")
    results = process_multiple_tickers(request.params)
    if not results:
        raise HTTPException(status_code=400, detail="Не удалось обработать ни одного тикера")
    return MultiTickerReturnsResponse(results=results)
