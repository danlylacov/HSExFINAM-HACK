import pandas as pd
from datetime import timedelta
from fastapi import HTTPException
from typing import Dict, Any, List
from collections import defaultdict
from backend_api.services.model_service import predict_single_candle

def process_multiple_tickers(input_candles: List[Dict[str, Any]]):
    results = []
    ticker_data = defaultdict(list)
    for candle in input_candles:
        ticker = candle.get('ticker', 'UNKNOWN')
        ticker_data[ticker].append(candle)
    for ticker, candles in ticker_data.items():
        print(f"Обрабатываем тикер: {ticker} ({len(candles)} записей)")
        candles_sorted = sorted(candles, key=lambda x: x.get('date', ''))
        base_close_price = candles_sorted[-1].get('close', 0)
        if base_close_price <= 0:
            print(f"⚠️  Пропускаем тикер {ticker}: некорректная базовая цена")
            continue
        predicted_candles = generate_20_candles_from_history(candles_sorted)
        returns = calculate_returns_from_predictions(predicted_candles, base_close_price)
        results.append({
            "ticker": ticker,
            "returns": returns
        })
    return results

def calculate_returns_from_predictions(predicted_candles: List[Dict[str, Any]], base_close_price: float) -> List[float]:
    returns = []
    for candle in predicted_candles:
        predicted_close = candle['close']
        return_rate = (predicted_close / base_close_price) - 1
        returns.append(round(return_rate, 6))
    return returns

def generate_20_candles_from_history(input_candles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not input_candles:
        raise ValueError("Пустой список входных свечей")
    df = pd.DataFrame(input_candles)
    from backend_api.utils.features import create_features
    df = create_features(df)
    df = df.bfill().ffill().fillna(0)
    last_date = pd.to_datetime(df['date'].iloc[-1])
    predicted_candles = []
    for i in range(20):
        last_row = df.iloc[-1].copy()
        predictions = predict_single_candle_from_row(last_row)
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
        new_row = last_row.copy()
        new_row.update(predictions)
        new_row['date'] = new_candle['date']
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df = create_features(df)
        df = df.bfill().ffill().fillna(0)
    return predicted_candles

def predict_single_candle_from_row(row_data: pd.Series) -> Dict[str, float]:
    try:
        df = pd.DataFrame([row_data])
        from backend_api.utils.features import create_features
        df = create_features(df)
        df = df.bfill().ffill().fillna(0)
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        exclude_columns = ['ticker', 'begin', 'open', 'high', 'low', 'close', 'volume']
        current_feature_columns = [col for col in numeric_columns if col not in exclude_columns]
        X = df[current_feature_columns]
        from backend_api.services.model_service import ensemble_models, scalers, feature_selectors, feature_columns, target_columns
        predictions = {}
        for target in target_columns:
            if target in ensemble_models:
                X_scaled = scalers[target].transform(X)
                X_selected = feature_selectors[target].transform(X_scaled)
                pred = ensemble_models[target].predict(X_selected)[0]
                predictions[target] = float(pred)
        return predictions
    except Exception as e:
        import traceback
        print(f"Ошибка предсказания: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Ошибка предсказания: {str(e)}")
