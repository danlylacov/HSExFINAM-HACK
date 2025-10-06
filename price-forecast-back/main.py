from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
import joblib
import os
import json
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Импорты для моделей
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor, ExtraTreesRegressor
from sklearn.linear_model import Ridge, Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import TimeSeriesSplit, cross_val_score

app = FastAPI(title="Price Prediction API", version="1.0.0")

# Модели и препроцессоры
ensemble_models = {}
scalers = {}
feature_selectors = {}
feature_columns = []

# Целевые переменные
target_columns = ['open', 'high', 'low', 'close', 'volume']

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
    # Параметры разделения данных
    train_size: Optional[int] = 25
    test_size: Optional[int] = None
    
    # Параметры Random Forest
    rf_n_estimators: Optional[int] = 200
    rf_max_depth: Optional[int] = 15
    rf_min_samples_split: Optional[int] = 5
    rf_min_samples_leaf: Optional[int] = 2
    
    # Параметры Gradient Boosting
    gb_n_estimators: Optional[int] = 200
    gb_learning_rate: Optional[float] = 0.1
    gb_max_depth: Optional[int] = 6
    gb_min_samples_split: Optional[int] = 5
    
    # Параметры Extra Trees
    et_n_estimators: Optional[int] = 150
    et_max_depth: Optional[int] = 15
    et_min_samples_split: Optional[int] = 5
    
    # Параметры Ridge/Lasso
    ridge_alpha: Optional[float] = 1.0
    lasso_alpha: Optional[float] = 0.1
    lasso_max_iter: Optional[int] = 2000
    
    # Веса для ансамбля
    ensemble_weights: Optional[List[float]] = [3, 3, 2, 1, 1]
    
    # Параметры кросс-валидации
    cv_splits: Optional[int] = 5
    
    # Параметры отбора признаков
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

def create_features(df):
    """Создание дополнительных признаков как в ноутбуке"""
    df = df.copy()
    
    # Лаговые признаки
    for col in ['close', 'volume', 'rsi', 'macd']:
        if col in df.columns:
            for lag in [1, 2, 3, 5]:
                df[f'{col}_lag_{lag}'] = df[col].shift(lag)
    
    # Скользящие статистики
    if 'close' in df.columns:
        for window in [5, 10, 20]:
            df[f'close_rolling_mean_{window}'] = df['close'].rolling(window).mean()
            df[f'close_rolling_std_{window}'] = df['close'].rolling(window).std()
            df[f'close_rolling_min_{window}'] = df['close'].rolling(window).min()
            df[f'close_rolling_max_{window}'] = df['close'].rolling(window).max()
    
    # Волатильность
    if all(col in df.columns for col in ['high', 'low']):
        df['volatility'] = (df['high'] - df['low']) / df['open']
    
    # Взаимодействия признаков
    if all(col in df.columns for col in ['rsi', 'macd']):
        df['rsi_macd_interaction'] = df['rsi'] * df['macd']
    
    return df

import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor

def send_callback(callback_url: str, payload: dict):
    """Отправка callback запроса"""
    try:
        response = requests.post(
            callback_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        print(f"Callback sent to {callback_url}: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending callback to {callback_url}: {e}")
        return False

async def process_combined_data_async(request: ProcessCombinedDataRequest) -> ProcessCombinedDataResponse:
    """
    Асинхронная обработка комбинированных данных с отправкой callback
    """
    try:
        # Извлекаем данные из запроса
        session_id = request.sessionId[0] if request.sessionId else "unknown"
        callback_urls = request.callbackUrl
        
        print(f"Обрабатываем данные для сессии: {session_id}")
        print(f"Callback URLs: {callback_urls}")
        
        # Обрабатываем каждую запись данных
        all_results = []
        
        for data_item in request.data:
            # Парсим данные из строки
            news_data_str = data_item.get("newsData", "{}")
            candle_data_str = data_item.get("candleData", "[]")
            
            try:
                # Парсим JSON данные
                news_data = json.loads(news_data_str)
                candle_data = json.loads(candle_data_str)
                
                # Преобразуем в формат для предсказания
                processed_data = convert_to_prediction_format(news_data, candle_data)
                
                if processed_data:
                    # Получаем предсказания
                    prediction_results = process_multiple_tickers(processed_data)
                    all_results.extend(prediction_results)
                
            except json.JSONDecodeError as e:
                print(f"Ошибка парсинга JSON для сессии {session_id}: {e}")
                continue
            except Exception as e:
                print(f"Ошибка обработки данных для сессии {session_id}: {e}")
                continue
        
        if not all_results:
            # Отправляем callback с ошибкой
            error_payload = {
                "sessionId": session_id,
                "status": "error",
                "errorMessage": "Не удалось обработать данные"
            }
            
            # Отправляем callback асинхронно
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as executor:
                for callback_url in callback_urls:
                    loop.run_in_executor(executor, send_callback, callback_url, error_payload)
            
            return ProcessCombinedDataResponse(
                sessionId=session_id,
                status="error",
                errorMessage="Не удалось обработать данные"
            )
        
        # Формируем результат в формате CSV
        csv_results = []
        for result in all_results:
            ticker = result.ticker
            returns = result.returns
            csv_line = f"{ticker}," + ",".join([f"{r:.6f}" for r in returns])
            csv_results.append(csv_line)
        
        prediction_csv = "\n".join(csv_results)
        
        # Отправляем callback с успешным результатом
        success_payload = {
            "sessionId": session_id,
            "status": "success",
            "prediction": prediction_csv
        }
        
        # Отправляем callback асинхронно
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            for callback_url in callback_urls:
                loop.run_in_executor(executor, send_callback, callback_url, success_payload)
        
        print(f"Успешно обработано {len(all_results)} тикеров для сессии {session_id}")
        
        return ProcessCombinedDataResponse(
            sessionId=session_id,
            status="success",
            prediction=prediction_csv
        )
        
    except Exception as e:
        import traceback
        print(f"Ошибка обработки запроса для сессии {session_id}: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        
        # Отправляем callback с ошибкой
        error_payload = {
            "sessionId": session_id,
            "status": "error",
            "errorMessage": str(e)
        }
        
        # Отправляем callback асинхронно
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            for callback_url in callback_urls:
                loop.run_in_executor(executor, send_callback, callback_url, error_payload)
        
        return ProcessCombinedDataResponse(
            sessionId=session_id,
            status="error",
            errorMessage=str(e)
        )

def convert_to_prediction_format(news_data: dict, candle_data: list) -> List[Dict[str, Any]]:
    """
    Преобразование данных из нового формата в формат для предсказания
    """
    try:
        # Извлекаем данные из news_data
        features = news_data.get("features", [])
        joined = news_data.get("joined", [])
        
        # Если есть joined данные, используем их
        if joined:
            result_params = []
            for item in joined:
                # Преобразуем данные в нужный формат
                record = {
                    "ticker": item.get("ticker", ""),
                    "date": item.get("date", ""),
                    "open": float(item.get("open", 0)),
                    "high": float(item.get("high", 0)),
                    "low": float(item.get("low", 0)),
                    "close": float(item.get("close", 0)),
                    "volume": float(item.get("volume", 0)),
                    "nn_news_sum": float(item.get("nn_news_sum", 0)),
                    "nn_news_mean": float(item.get("nn_news_mean", 0)),
                    "nn_news_max": float(item.get("nn_news_max", 0)),
                    "nn_news_count": int(item.get("nn_news_count", 0)),
                    "sentiment_mean": float(item.get("sentiment_mean", 0)),
                    "sentiment_sum": float(item.get("sentiment_sum", 0)),
                    "sentiment_count": int(item.get("sentiment_count", 0)),
                    "sentiment_positive_count": int(item.get("sentiment_positive_count", 0)),
                    "sentiment_negative_count": int(item.get("sentiment_negative_count", 0)),
                    "sentiment_neutral_count": int(item.get("sentiment_neutral_count", 0)),
                    "rsi": 50.0,  # Значение по умолчанию
                    "macd": 0.0,
                    "cci": 0.0,
                    "ema9": float(item.get("close", 0)),
                    "ema50": float(item.get("close", 0)),
                    "areThreeWhiteSoldiers": 0,
                    "areThreeBlackCrows": 0,
                    "doji": 0,
                    "bearishEngulfing": 0,
                    "bullishEngulfing": 0
                }
                result_params.append(record)
            return result_params
        
        # Если нет joined данных, обрабатываем candle_data
        elif candle_data:
            result_params = []
            for candle in candle_data:
                # Парсим данные свечи
                record = {
                    "ticker": candle.get("ticker", ""),
                    "date": candle.get("begin", ""),
                    "open": float(candle.get("open", 0)),
                    "high": float(candle.get("high", 0)),
                    "low": float(candle.get("low", 0)),
                    "close": float(candle.get("close", 0)),
                    "volume": float(candle.get("volume", 0)),
                    "nn_news_sum": 0.0,
                    "nn_news_mean": 0.0,
                    "nn_news_max": 0.0,
                    "nn_news_count": 0,
                    "sentiment_mean": 0.0,
                    "sentiment_sum": 0.0,
                    "sentiment_count": 0,
                    "sentiment_positive_count": 0,
                    "sentiment_negative_count": 0,
                    "sentiment_neutral_count": 0,
                    "rsi": float(candle.get("rsi", 50.0)),
                    "macd": float(candle.get("macd", 0.0)),
                    "cci": float(candle.get("cci", 0.0)),
                    "ema9": float(candle.get("ema9", candle.get("close", 0))),
                    "ema50": float(candle.get("ema50", candle.get("close", 0))),
                    "areThreeWhiteSoldiers": 1 if candle.get("areThreeWhiteSoldiers", False) else 0,
                    "areThreeBlackCrows": 1 if candle.get("areThreeBlackCrows", False) else 0,
                    "doji": 1 if candle.get("isDoji", False) else 0,
                    "bearishEngulfing": 1 if candle.get("isBearishEngulfing", False) else 0,
                    "bullishEngulfing": 1 if candle.get("isBullishEngulfing", False) else 0
                }
                result_params.append(record)
            return result_params
        
        return []
        
    except Exception as e:
        print(f"Ошибка преобразования данных: {e}")
        return []

def train_models_with_config(data_file: str, config: TrainingConfig) -> TrainingResponse:
    """Обучение моделей с настраиваемыми параметрами"""
    try:
        # Загружаем данные
        if data_file.endswith('.csv'):
            data = pd.read_csv(data_file)
        elif data_file.endswith('.json'):
            data = pd.read_json(data_file)
        else:
            raise ValueError("Неподдерживаемый формат файла")
        
        # Разделяем данные
        if config.test_size is None:
            train_df = data[:config.train_size]
            test_df = data[config.train_size:]
        else:
            train_df = data[:config.train_size]
            test_df = data[config.train_size:config.train_size + config.test_size]
        
        # Преобразование дат
        if 'begin' in train_df.columns:
            train_df['begin'] = pd.to_datetime(train_df['begin'])
            test_df['begin'] = pd.to_datetime(test_df['begin'])
            train_df = train_df.sort_values('begin')
            test_df = test_df.sort_values('begin')
        
        # Создание дополнительных признаков
        train_df = create_features(train_df)
        test_df = create_features(test_df)
        
        # Заполнение пропусков
        train_df = train_df.bfill().ffill().fillna(0)
        test_df = test_df.bfill().ffill().fillna(0)
        
        # Автоматическое определение ЧИСЛОВЫХ признаков
        exclude_columns = ['ticker', 'begin'] + target_columns
        numeric_columns = train_df.select_dtypes(include=[np.number]).columns.tolist()
        feature_columns = [col for col in numeric_columns if col not in exclude_columns]
        
        # Создаем папку для моделей
        os.makedirs('models', exist_ok=True)
        
        # Обучение моделей
        ensemble_models = {}
        scalers = {}
        feature_selectors = {}
        training_metrics = {}
        
        for target in target_columns:
            print(f"Обучение модели для {target}...")
            
            # Подготовка данных
            X_train = train_df[feature_columns]
            y_train = train_df[target]
            X_test = test_df[feature_columns]
            
            # Удаляем строки с пропусками
            valid_indices = ~y_train.isnull()
            X_train = X_train[valid_indices]
            y_train = y_train[valid_indices]
            
            # Масштабирование
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            scalers[target] = scaler
            
            # Отбор признаков
            selector = SelectFromModel(
                RandomForestRegressor(
                    n_estimators=config.feature_selection_n_estimators, 
                    random_state=42, 
                    n_jobs=-1
                ),
                threshold=config.feature_selection_threshold
            )
            X_train_selected = selector.fit_transform(X_train_scaled, y_train)
            X_test_selected = selector.transform(X_test_scaled)
            feature_selectors[target] = selector
            
            # Создание моделей с настраиваемыми параметрами
            models = [
                ('rf', RandomForestRegressor(
                    n_estimators=config.rf_n_estimators,
                    max_depth=config.rf_max_depth,
                    min_samples_split=config.rf_min_samples_split,
                    min_samples_leaf=config.rf_min_samples_leaf,
                    random_state=42,
                    n_jobs=-1
                )),
                ('gb', GradientBoostingRegressor(
                    n_estimators=config.gb_n_estimators,
                    learning_rate=config.gb_learning_rate,
                    max_depth=config.gb_max_depth,
                    min_samples_split=config.gb_min_samples_split,
                    random_state=42
                )),
                ('et', ExtraTreesRegressor(
                    n_estimators=config.et_n_estimators,
                    max_depth=config.et_max_depth,
                    min_samples_split=config.et_min_samples_split,
                    random_state=42,
                    n_jobs=-1
                )),
                ('ridge', Ridge(alpha=config.ridge_alpha, random_state=42)),
                ('lasso', Lasso(alpha=config.lasso_alpha, random_state=42, max_iter=config.lasso_max_iter))
            ]
            
            # Ансамбль с настраиваемыми весами
            ensemble = VotingRegressor(
                estimators=models,
                weights=config.ensemble_weights
            )
            
            # Кросс-валидация
            tscv = TimeSeriesSplit(n_splits=config.cv_splits)
            cv_scores = cross_val_score(ensemble, X_train_selected, y_train, 
                                       cv=tscv, scoring='neg_mean_absolute_error')
            
            # Обучение
            ensemble.fit(X_train_selected, y_train)
            
            # Предсказание на тесте
            pred = ensemble.predict(X_test_selected)
            
            # Сохранение модели
            ensemble_models[target] = ensemble
            
            # Сохраняем модели
            joblib.dump(ensemble, f'models/{target}_model.pkl')
            joblib.dump(scaler, f'models/{target}_scaler.pkl')
            joblib.dump(selector, f'models/{target}_selector.pkl')
            
            # Сохраняем метрики
            training_metrics[target] = {
                'cv_mae_mean': -cv_scores.mean(),
                'cv_mae_std': cv_scores.std(),
                'selected_features': X_train_selected.shape[1],
                'total_features': X_train_scaled.shape[1]
            }
            
            print(f"Модель для {target} обучена. CV MAE: {-cv_scores.mean():.4f}")
        
        # Сохраняем список признаков
        joblib.dump(feature_columns, 'models/feature_columns.pkl')
        
        return TrainingResponse(
            status="success",
            message=f"Обучено {len(ensemble_models)} моделей",
            models_trained=list(ensemble_models.keys()),
            training_metrics=training_metrics,
            feature_count=len(feature_columns),
            selected_features_count=sum([m['selected_features'] for m in training_metrics.values()]) // len(training_metrics)
        )
        
    except Exception as e:
        import traceback
        print(f"Ошибка обучения: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Ошибка обучения: {str(e)}")

def load_models():
    """Загрузка обученных моделей"""
    global ensemble_models, scalers, feature_selectors, feature_columns
    
    try:
        # Загружаем модели для каждой целевой переменной
        for target in target_columns:
            model_path = f"models/{target}_model.pkl"
            scaler_path = f"models/{target}_scaler.pkl"
            selector_path = f"models/{target}_selector.pkl"
            
            if os.path.exists(model_path) and os.path.exists(scaler_path) and os.path.exists(selector_path):
                print(f"Загружаем модель для {target}...")
                ensemble_models[target] = joblib.load(model_path)
                scalers[target] = joblib.load(scaler_path)
                feature_selectors[target] = joblib.load(selector_path)
                print(f"Модель для {target} загружена успешно")
            else:
                print(f"Файлы для {target} не найдены: {model_path}, {scaler_path}, {selector_path}")
        
        # Загружаем список признаков
        if os.path.exists("models/feature_columns.pkl"):
            feature_columns = joblib.load("models/feature_columns.pkl")
            print(f"Загружено {len(feature_columns)} признаков")
        else:
            print("Файл feature_columns.pkl не найден")
        
        print(f"Загружено {len(ensemble_models)} моделей")
        print(f"Доступные модели: {list(ensemble_models.keys())}")
        return len(ensemble_models) > 0
        
    except Exception as e:
        import traceback
        print(f"Ошибка загрузки моделей: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

def predict_single_candle(input_data: Dict[str, Any]) -> Dict[str, float]:
    """Предсказание одной свечи"""
    try:
        # Преобразуем входные данные в DataFrame
        df = pd.DataFrame([input_data])
        
        # Создаем признаки
        df = create_features(df)
        
        # Заполняем пропуски
        df = df.bfill().ffill()
        
        # Дополнительная проверка на NaN
        df = df.fillna(0)  # Заполняем оставшиеся NaN нулями
        
        # Выбираем только числовые признаки
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        exclude_columns = ['ticker', 'begin'] + target_columns
        current_feature_columns = [col for col in numeric_columns if col not in exclude_columns]
        
        # Убеждаемся, что все признаки из модели присутствуют
        X = df[current_feature_columns]
        
        # Предсказания для каждой целевой переменной
        predictions = {}
        
        for target in target_columns:
            if target in ensemble_models:
                # Масштабирование
                X_scaled = scalers[target].transform(X)
                
                # Отбор признаков
                X_selected = feature_selectors[target].transform(X_scaled)
                
                # Предсказание
                pred = ensemble_models[target].predict(X_selected)[0]
                predictions[target] = float(pred)
        
        return predictions
        
    except Exception as e:
        import traceback
        print(f"Ошибка предсказания: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Ошибка предсказания: {str(e)}")

def process_multiple_tickers(input_candles: List[Dict[str, Any]]) -> List[ReturnsResponse]:
    """
    Обработка данных с несколькими тикерами
    
    Args:
        input_candles: Список свечей с разными тикерами
    
    Returns:
        Список результатов для каждого тикера
    """
    from collections import defaultdict
    
    # Группируем данные по тикерам
    ticker_data = defaultdict(list)
    for candle in input_candles:
        ticker = candle.get('ticker', 'UNKNOWN')
        ticker_data[ticker].append(candle)
    
    results = []
    
    for ticker, candles in ticker_data.items():
        print(f"Обрабатываем тикер: {ticker} ({len(candles)} записей)")
        
        # Сортируем по дате для каждого тикера
        candles_sorted = sorted(candles, key=lambda x: x.get('date', ''))
        
        # Получаем базовую цену закрытия (последняя цена для этого тикера)
        base_close_price = candles_sorted[-1].get('close', 0)
        if base_close_price <= 0:
            print(f"⚠️  Пропускаем тикер {ticker}: некорректная базовая цена")
            continue
        
        print(f"  Базовая цена закрытия: {base_close_price}")
        
        # Генерируем 20 следующих свечей для этого тикера
        predicted_candles = generate_20_candles_from_history(candles_sorted)
        
        # Рассчитываем доходности
        returns = calculate_returns_from_predictions(predicted_candles, base_close_price)
        
        print(f"  Рассчитаны доходности: {len(returns)} значений")
        print(f"  Диапазон доходностей: {min(returns):.6f} до {max(returns):.6f}")
        
        results.append(ReturnsResponse(ticker=ticker, returns=returns))
    
    return results

def calculate_returns_from_predictions(predicted_candles: List[Dict[str, Any]], base_close_price: float) -> List[float]:
    """
    Расчет доходностей p_i = (close_{t+i} / close_t) - 1
    
    Args:
        predicted_candles: Список предсказанных свечей
        base_close_price: Базовая цена закрытия (close_t)
    
    Returns:
        Список доходностей [p1, p2, ..., p20]
    """
    returns = []
    for candle in predicted_candles:
        predicted_close = candle['close']
        return_rate = (predicted_close / base_close_price) - 1
        returns.append(round(return_rate, 6))  # Округляем до 6 знаков после запятой
    return returns

def generate_20_candles_from_history(input_candles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Генерация 20 свечей на основе истории входных свечей"""
    if not input_candles:
        raise ValueError("Пустой список входных свечей")
    
    # Преобразуем входные свечи в DataFrame
    df = pd.DataFrame(input_candles)
    
    # Создаем признаки для всей истории
    df = create_features(df)
    
    # Заполняем пропуски
    df = df.bfill().ffill().fillna(0)
    
    # Получаем последнюю дату
    last_date = pd.to_datetime(df['date'].iloc[-1])
    
    # Предсказываем следующие 20 свечей
    predicted_candles = []
    
    for i in range(20):
        # Берем последнюю строку для предсказания
        last_row = df.iloc[-1].copy()
        
        # Предсказываем следующую свечу
        predictions = predict_single_candle_from_row(last_row)
        
        # Создаем новую свечу
        new_candle = {
            'date': (last_date + timedelta(days=i+1)).strftime('%Y-%m-%d'),
            'ticker': last_row.get('ticker', 'UNKNOWN'),
            'open': predictions.get('open', 0),
            'high': predictions.get('high', 0),
            'low': predictions.get('low', 0),
            'close': predictions.get('close', 0),
            'volume': predictions.get('volume', 0)
        }
        
        predicted_candles.append(new_candle)
        
        # Добавляем новую свечу к истории для следующего предсказания
        new_row = last_row.copy()
        new_row.update(predictions)
        new_row['date'] = new_candle['date']
        
        # Добавляем новую строку в DataFrame
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        
        # Пересчитываем признаки для новой строки
        df = create_features(df)
        df = df.bfill().ffill().fillna(0)
    
    return predicted_candles

def predict_single_candle_from_row(row_data: pd.Series) -> Dict[str, float]:
    """Предсказание одной свечи на основе строки данных"""
    try:
        # Преобразуем в DataFrame
        df = pd.DataFrame([row_data])
        
        # Выбираем только числовые признаки
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        exclude_columns = ['ticker', 'begin'] + target_columns
        current_feature_columns = [col for col in numeric_columns if col not in exclude_columns]
        
        # Убеждаемся, что все признаки из модели присутствуют
        X = df[current_feature_columns]
        
        # Предсказания для каждой целевой переменной
        predictions = {}
        
        for target in target_columns:
            if target in ensemble_models:
                # Масштабирование
                X_scaled = scalers[target].transform(X)
                
                # Отбор признаков
                X_selected = feature_selectors[target].transform(X_scaled)
                
                # Предсказание
                pred = ensemble_models[target].predict(X_selected)[0]
                predictions[target] = float(pred)
        
        return predictions
        
    except Exception as e:
        import traceback
        print(f"Ошибка предсказания: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Ошибка предсказания: {str(e)}")

@app.on_event("startup")
async def startup_event():
    """Инициализация при запуске"""
    if not load_models():
        print("Предупреждение: Модели не загружены. Создайте модели сначала.")

@app.get("/")
async def root():
    return {"message": "Price Prediction API", "status": "running"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "models_loaded": len(ensemble_models),
        "available_targets": list(ensemble_models.keys())
    }

@app.post("/process-combined-data", response_model=ProcessCombinedDataResponse)
async def process_combined_data_endpoint(request: ProcessCombinedDataRequest):
    """
    Обработка комбинированных данных с отправкой callback
    
    Входной формат:
    {
        "data": [
            {
                "sessionId": "f8296fe5-8340-4aa5-a433-266c1b7d07b6",
                "newsData": "{\"features\": [...], \"joined\": [...], \"summary\": {...}}",
                "candleData": "[CandleDtoRs(...), ...]"
            }
        ],
        "callbackUrl": ["http://176.57.217.27:8087/api/v1/callbacks/prediction"],
        "sessionId": ["f8296fe5-8340-4aa5-a433-266c1b7d07b6"]
    }
    
    Возвращает:
    {
        "sessionId": "f8296fe5-8340-4aa5-a433-266c1b7d07b6",
        "status": "success",
        "prediction": "AFLT,p1,p2,...,p20\nSBER,p1,p2,...,p20"
    }
    
    И отправляет callback на указанный URL с результатами предсказания
    """
    try:
        result = await process_combined_data_async(request)
        return result
    except Exception as e:
        import traceback
        print(f"Ошибка обработки комбинированных данных: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        
        # Отправляем callback с ошибкой
        session_id = request.sessionId[0] if request.sessionId else "unknown"
        error_payload = {
            "sessionId": session_id,
            "status": "error",
            "errorMessage": str(e)
        }
        
        # Отправляем callback асинхронно
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            for callback_url in request.callbackUrl:
                loop.run_in_executor(executor, send_callback, callback_url, error_payload)
        
        raise HTTPException(status_code=500, detail=f"Ошибка обработки данных: {str(e)}")

@app.post("/upload-data", response_model=DataUploadResponse)
async def upload_data(file: UploadFile = File(...)):
    """
    Загрузка данных для обучения модели
    
    Поддерживаемые форматы: CSV, JSON
    """
    try:
        # Проверяем формат файла
        if not file.filename.endswith(('.csv', '.json')):
            raise HTTPException(status_code=400, detail="Неподдерживаемый формат файла. Используйте CSV или JSON")
        
        # Сохраняем файл
        file_path = f"data/{file.filename}"
        os.makedirs("data", exist_ok=True)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Читаем данные для проверки
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_json(file_path)
        
        return DataUploadResponse(
            status="success",
            message=f"Файл {file.filename} успешно загружен",
            filename=file.filename,
            rows_count=len(df),
            columns_count=len(df.columns),
            columns=list(df.columns)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка загрузки файла: {str(e)}")

@app.post("/train", response_model=TrainingResponse)
async def train_models(
    filename: str = Form(...),
    config: str = Form(...)
):
    """
    Обучение модели с настраиваемыми параметрами
    
    Параметры:
    - filename: имя файла с данными (должен быть загружен через /upload-data)
    - config: JSON строка с параметрами обучения
    """
    try:
        # Проверяем существование файла
        file_path = f"data/{filename}"
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"Файл {filename} не найден. Сначала загрузите данные через /upload-data")
        
        # Парсим конфигурацию
        try:
            config_dict = json.loads(config)
            training_config = TrainingConfig(**config_dict)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Неверный формат JSON конфигурации")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Ошибка в конфигурации: {str(e)}")
        
        # Обучаем модель
        result = train_models_with_config(file_path, training_config)
        
        # Перезагружаем модели в память
        load_models()
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обучения: {str(e)}")

@app.get("/training-config")
async def get_default_training_config():
    """
    Получить конфигурацию по умолчанию для обучения
    """
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

@app.get("/data-files")
async def list_data_files():
    """
    Получить список загруженных файлов с данными
    """
    try:
        data_dir = "data"
        if not os.path.exists(data_dir):
            return {"files": [], "message": "Папка data не существует"}
        
        files = []
        for filename in os.listdir(data_dir):
            if filename.endswith(('.csv', '.json')):
                file_path = os.path.join(data_dir, filename)
                file_size = os.path.getsize(file_path)
                files.append({
                    "filename": filename,
                    "size_bytes": file_size,
                    "size_mb": round(file_size / (1024 * 1024), 2)
                })
        
        return {"files": files}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения списка файлов: {str(e)}")

@app.post("/predict", response_model=MultiTickerReturnsResponse)
async def predict_returns(request: PredictionRequest):
    """
    Предсказание доходностей следующих 20 периодов на основе истории входных свечей
    
    Поддерживает как один тикер, так и несколько тикеров одновременно.
    
    Входной формат - массив исторических свечей:
    {
        "params": [
            {
                "ticker": "AFLT",
                "date": "2025-01-01",
                "nn_news_sum": 1.2,
                "nn_news_mean": 0.03,
                "nn_news_max": 0.18,
                "nn_news_count": 43,
                "sentiment_mean": 0.5,
                "sentiment_sum": 20.0,
                "sentiment_count": 40,
                "sentiment_positive_count": 20,
                "sentiment_negative_count": 10,
                "sentiment_neutral_count": 10,
                "rsi": 50.0,
                "macd": 0.5,
                "cci": 0.0,
                "ema9": 100.0,
                "ema50": 100.0,
                "areThreeWhiteSoldiers": 0,
                "areThreeBlackCrows": 0,
                "doji": 0,
                "bearishEngulfing": 0,
                "bullishEngulfing": 0,
                "open": 100.0,
                "high": 105.0,
                "low": 95.0,
                "close": 102.0,
                "volume": 1000000
            },
            // ... еще исторические свечи (может быть разных тикеров)
        ]
    }
    
    Возвращает доходности для каждого тикера:
    {
        "results": [
            {
                "ticker": "AFLT",
                "returns": [0.0234, -0.0156, 0.0456, ...]  // p1, p2, ..., p20
            },
            {
                "ticker": "SBER", 
                "returns": [0.0123, 0.0234, -0.0100, ...]  // p1, p2, ..., p20
            }
        ]
    }
    
    где p_i = (close_{t+i} / close_t) - 1 для каждого тикера отдельно
    """
    try:
        if not ensemble_models:
            raise HTTPException(status_code=503, detail="Модели не загружены")
        
        if not request.params:
            raise HTTPException(status_code=400, detail="Пустой список параметров")
        
        print(f"Обрабатываем {len(request.params)} исторических свечей для расчета доходностей")
        
        # Обрабатываем все тикеры
        results = process_multiple_tickers(request.params)
        
        if not results:
            raise HTTPException(status_code=400, detail="Не удалось обработать ни одного тикера")
        
        print(f"Успешно обработано {len(results)} тикеров")
        
        return MultiTickerReturnsResponse(results=results)
        
    except Exception as e:
        import traceback
        print(f"Ошибка обработки запроса: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Ошибка обработки запроса: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8009)
