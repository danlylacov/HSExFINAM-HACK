#!/usr/bin/env python3
"""
Тест нового эндпоинта для обработки комбинированных данных
"""

import requests
import json

def test_combined_data_endpoint():
    """Тестирование эндпоинта обработки комбинированных данных"""
    base_url = "http://localhost:8009"
    
    # Тестовые данные
    test_news_data = [
        {
            "date": "2025-01-01",
            "ticker": "AFLT",
            "nn_news_sum": 1.2,
            "nn_news_mean": 0.03,
            "nn_news_max": 0.18,
            "nn_news_count": 43,
            "sentiment_mean": 0.5,
            "sentiment_sum": 20.0,
            "sentiment_count": 40,
            "sentiment_positive_count": 20,
            "sentiment_negative_count": 10,
            "sentiment_neutral_count": 10
        },
        {
            "date": "2025-01-02",
            "ticker": "AFLT",
            "nn_news_sum": 1.5,
            "nn_news_mean": 0.04,
            "nn_news_max": 0.20,
            "nn_news_count": 45,
            "sentiment_mean": 0.6,
            "sentiment_sum": 25.0,
            "sentiment_count": 42,
            "sentiment_positive_count": 25,
            "sentiment_negative_count": 8,
            "sentiment_neutral_count": 9
        }
    ]
    
    test_candle_data = [
        {
            "date": "2025-01-01",
            "ticker": "AFLT",
            "open": 100.0,
            "high": 105.0,
            "low": 95.0,
            "close": 102.0,
            "volume": 1000000,
            "rsi": 50.0,
            "macd": 0.5,
            "cci": 0.0,
            "ema9": 100.0,
            "ema50": 100.0,
            "areThreeWhiteSoldiers": 0,
            "areThreeBlackCrows": 0,
            "doji": 0,
            "bearishEngulfing": 0,
            "bullishEngulfing": 0
        },
        {
            "date": "2025-01-02",
            "ticker": "AFLT",
            "open": 102.0,
            "high": 107.0,
            "low": 97.0,
            "close": 104.0,
            "volume": 1200000,
            "rsi": 55.0,
            "macd": 0.6,
            "cci": 0.1,
            "ema9": 101.0,
            "ema50": 100.5,
            "areThreeWhiteSoldiers": 0,
            "areThreeBlackCrows": 0,
            "doji": 0,
            "bearishEngulfing": 0,
            "bullishEngulfing": 0
        },
        {
            "date": "2025-01-03",
            "ticker": "AFLT",
            "open": 104.0,
            "high": 109.0,
            "low": 99.0,
            "close": 106.0,
            "volume": 1100000,
            "rsi": 60.0,
            "macd": 0.7,
            "cci": 0.2,
            "ema9": 102.0,
            "ema50": 101.0,
            "areThreeWhiteSoldiers": 0,
            "areThreeBlackCrows": 0,
            "doji": 0,
            "bearishEngulfing": 0,
            "bullishEngulfing": 0
        }
    ]
    
    # Создаем запрос
    request_data = {
        "sessionId": "test_session_123",
        "newsData": json.dumps(test_news_data),
        "candleData": json.dumps(test_candle_data)
    }
    
    print("🚀 Тестирование эндпоинта обработки комбинированных данных")
    print("=" * 60)
    
    try:
        # Проверяем здоровье API
        print("1. Проверка здоровья API...")
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ API здоров: {health_data}")
        else:
            print(f"❌ API недоступен: {response.status_code}")
            return False
        
        # Тестируем обработку комбинированных данных
        print("\n2. Тестирование обработки комбинированных данных...")
        response = requests.post(
            f"{base_url}/process-combined-data",
            json=request_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Данные успешно обработаны!")
            
            # Анализируем результат
            params = result.get('params', [])
            print(f"\n📊 Результат обработки:")
            print(f"   Количество записей: {len(params)}")
            
            for i, param in enumerate(params):
                print(f"\n   Запись {i+1}:")
                print(f"     Дата: {param.get('date')}")
                print(f"     Тикер: {param.get('ticker')}")
                print(f"     Цена закрытия: {param.get('close')}")
                print(f"     Новостная сумма: {param.get('nn_news_sum')}")
                print(f"     Сентимент: {param.get('sentiment_mean')}")
                print(f"     RSI: {param.get('rsi')}")
                print(f"     MACD: {param.get('macd')}")
            
            # Проверяем логику объединения
            print(f"\n🔍 Анализ логики объединения:")
            
            # Проверяем первую запись (должна иметь новости)
            first_record = params[0]
            if first_record.get('nn_news_sum') > 0:
                print("   ✅ Первая запись: новости найдены и объединены")
            else:
                print("   ❌ Первая запись: новости не найдены")
            
            # Проверяем вторую запись (должна иметь новости)
            second_record = params[1]
            if second_record.get('nn_news_sum') > 0:
                print("   ✅ Вторая запись: новости найдены и объединены")
            else:
                print("   ❌ Вторая запись: новости не найдены")
            
            # Проверяем третью запись (не должно быть новостей)
            third_record = params[2]
            if third_record.get('nn_news_sum') == 0:
                print("   ✅ Третья запись: новости не найдены, поля установлены в 0")
            else:
                print("   ❌ Третья запись: неожиданно найдены новости")
            
            return True
            
        else:
            print(f"❌ Ошибка обработки: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Не удается подключиться к API. Убедитесь, что сервер запущен.")
        return False
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        return False

if __name__ == "__main__":
    success = test_combined_data_endpoint()
    if success:
        print("\n🎉 Тест пройден успешно!")
        print("✅ Эндпоинт обработки комбинированных данных работает корректно!")
    else:
        print("\n💥 Тест не пройден!")
