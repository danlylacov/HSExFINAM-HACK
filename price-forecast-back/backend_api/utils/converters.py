from typing import List, Dict, Any

def convert_to_prediction_format(news_data: dict, candle_data: list) -> List[Dict[str, Any]]:
    try:
        result_params = []
        features = news_data.get("features", [])
        joined = news_data.get("joined", [])
        # Приоритет: используем joined данные, если они есть
        if joined:
            for item in joined:
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
                    "rsi": 50.0,  # default
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
        elif candle_data:
            for candle in candle_data:
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
        elif features:
            for item in features:
                record = {
                    "ticker": item.get("ticker", ""),
                    "date": item.get("date", ""),
                    "open": 0.0,
                    "high": 0.0,
                    "low": 0.0,
                    "close": 0.0,
                    "volume": 0.0,
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
                    "rsi": 50.0,
                    "macd": 0.0,
                    "cci": 0.0,
                    "ema9": 0.0,
                    "ema50": 0.0,
                    "areThreeWhiteSoldiers": 0,
                    "areThreeBlackCrows": 0,
                    "doji": 0,
                    "bearishEngulfing": 0,
                    "bullishEngulfing": 0
                }
                result_params.append(record)
        return result_params
    except Exception as e:
        print(f"Ошибка преобразования данных: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return []
