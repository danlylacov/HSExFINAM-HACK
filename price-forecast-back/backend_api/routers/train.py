from fastapi import APIRouter, HTTPException, Form
from backend_api.models.schemas import TrainingConfig, TrainingResponse
from backend_api.services.model_service import train_models_with_config, load_models
import json

router = APIRouter()

@router.post("/train", response_model=TrainingResponse)
async def train_models(
    filename: str = Form(...),
    config: str = Form(...)
):
    try:
        file_path = f"data/{filename}"
        config_dict = json.loads(config)
        training_config = TrainingConfig(**config_dict)
        result = train_models_with_config(file_path, training_config)
        load_models() # reload state
        return result
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Неверный формат JSON конфигурации")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обучения: {str(e)}")

@router.get("/training-config")
async def get_default_training_config():
    default_config = TrainingConfig()
    return {
        "default_config": default_config.dict(),
        "description": {
            "train_size": "Количество записей для обучения",
            "test_size": "Количество записей для тестирования (None = все остальные)",
            "rf_n_estimators": "Количество деревьев в Random Forest",
            "rf_max_depth": "Максимальная глубина деревьев в Random Forest",
            "gb_n_estimators": "Количество деревьев в Gradient Boosting",
            "gb_learning_rate": "Скорость обучения в Gradient Boosting",
            "ensemble_weights": "Веса для ансамбля [RF, GB, ET, Ridge, Lasso]",
            "cv_splits": "Количество фолдов для кросс-валидации"
        }
    }
