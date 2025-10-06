#!/usr/bin/env python3
"""
Тест нового бэкенда с моделью доходностей
"""

import requests
import json
import time

def test_new_backend():
    """Тестирование нового бэкенда"""
    base_url = "http://localhost:8009"
    
    # Тестовые данные
    test_data = {
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
            {
                "ticker": "AFLT",
                "date": "2025-01-02",
                "nn_news_sum": 1.5,
                "nn_news_mean": 0.04,
                "nn_news_max": 0.20,
                "nn_news_count": 45,
                "sentiment_mean": 0.6,
                "sentiment_sum": 25.0,
                "sentiment_count": 42,
                "sentiment_positive_count": 25,
                "sentiment_negative_count": 8,
                "sentiment_neutral_count": 9,
                "rsi": 55.0,
                "macd": 0.6,
                "cci": 0.1,
                "ema9": 101.0,
                "ema50": 100.5,
                "areThreeWhiteSoldiers": 0,
                "areThreeBlackCrows": 0,
                "doji": 0,
                "bearishEngulfing": 0,
                "bullishEngulfing": 0,
                "open": 102.0,
                "high": 107.0,
                "low": 97.0,
                "close": 104.0,
                "volume": 1200000
            }
        ]
    }
    
    print("🚀 Тестирование нового бэкенда с моделью доходностей")
    print("=" * 60)
    
    try:
        # Проверяем здоровье API
        print("1. Проверка здоровья API...")
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ API здоров: {health_data}")
        else:
            print(f"❌ API недоступен: {response.status_code}")
            return False
        
        # Тестируем предсказания
        print("\n2. Тестирование предсказаний...")
        response = requests.post(
            f"{base_url}/predict",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            predictions = response.json()
            print(f"✅ Предсказания получены: {len(predictions['predictions'])} свечей")
            
            # Анализируем предсказания
            first_prediction = predictions['predictions'][0]
            print(f"\n📊 Первое предсказание:")
            print(f"   Дата: {first_prediction['date']}")
            print(f"   Open: {first_prediction['open']:.2f}")
            print(f"   High: {first_prediction['high']:.2f}")
            print(f"   Low: {first_prediction['low']:.2f}")
            print(f"   Close: {first_prediction['close']:.2f}")
            print(f"   Volume: {first_prediction['volume']:.0f}")
            
            # Проверяем логику доходностей
            last_close = test_data['params'][-1]['close']
            predicted_close = first_prediction['close']
            return_rate = (predicted_close / last_close) - 1
            
            print(f"\n📈 Анализ доходности:")
            print(f"   Последняя цена: {last_close:.2f}")
            print(f"   Предсказанная цена: {predicted_close:.2f}")
            print(f"   Доходность: {return_rate:.4f} ({return_rate*100:.2f}%)")
            
            # Проверяем разумность предсказаний
            if abs(return_rate) < 0.2:  # Доходность в пределах 20%
                print("✅ Доходность в разумных пределах")
            else:
                print("⚠️  Доходность может быть слишком экстремальной")
            
            return True
            
        else:
            print(f"❌ Ошибка предсказания: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Не удается подключиться к API. Убедитесь, что сервер запущен.")
        return False
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        return False

if __name__ == "__main__":
    success = test_new_backend()
    if success:
        print("\n🎉 Тест пройден успешно!")
    else:
        print("\n💥 Тест не пройден!")
