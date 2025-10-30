from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class PredictionRequest(BaseModel):
    params: List[Dict[str, Any]]

class PredictionResponse(BaseModel):
    predictions: List[Dict[str, Any]]

class ReturnsResponse(BaseModel):
    ticker: str
    returns: List[float]  # p1, p2, ..., p20

class MultiTickerReturnsResponse(BaseModel):
    results: List[ReturnsResponse]  # Результаты для каждого тикера

class ProcessCombinedDataRequest(BaseModel):
    data: List[Dict[str, Any]]
    callbackUrl: List[str]
    sessionId: List[str]

class ProcessCombinedDataResponse(BaseModel):
    sessionId: str
    status: str
    prediction: Optional[str] = None
    errorMessage: Optional[str] = None

class CombinedData(BaseModel):
    sessionId: str
    newsData: str
    candleData: str

class CombinedDataResponse(BaseModel):
    params: List[Dict[str, Any]]

class TrainingConfig(BaseModel):
    train_size: Optional[int] = 25
    test_size: Optional[int] = None
    rf_n_estimators: Optional[int] = 200
    rf_max_depth: Optional[int] = 15
    rf_min_samples_split: Optional[int] = 5
    rf_min_samples_leaf: Optional[int] = 2
    gb_n_estimators: Optional[int] = 200
    gb_learning_rate: Optional[float] = 0.1
    gb_max_depth: Optional[int] = 6
    gb_min_samples_split: Optional[int] = 5
    et_n_estimators: Optional[int] = 150
    et_max_depth: Optional[int] = 15
    et_min_samples_split: Optional[int] = 5
    ridge_alpha: Optional[float] = 1.0
    lasso_alpha: Optional[float] = 0.1
    lasso_max_iter: Optional[int] = 2000
    ensemble_weights: Optional[List[float]] = [3, 3, 2, 1, 1]
    cv_splits: Optional[int] = 5
    feature_selection_threshold: Optional[str] = 'median'
    feature_selection_n_estimators: Optional[int] = 50

class TrainingResponse(BaseModel):
    status: str
    message: str
    models_trained: List[str]
    training_metrics: Dict[str, Any]
    feature_count: int
    selected_features_count: int

class DataUploadResponse(BaseModel):
    status: str
    message: str
    filename: str
    rows_count: int
    columns_count: int
    columns: List[str]
