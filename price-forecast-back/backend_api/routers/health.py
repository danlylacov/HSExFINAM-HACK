from fastapi import APIRouter
from backend_api.services.model_service import ensemble_models

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Price Prediction API", "status": "running"}

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "models_loaded": len(ensemble_models),
        "available_targets": list(ensemble_models.keys())
    }
