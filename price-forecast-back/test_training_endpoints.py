import requests
import json
import pandas as pd
import numpy as np

# Создаем тестовые данные
def create_test_data():
    """Создание тестовых данных для обучения"""
    np.random.seed(42)
    n_samples = 100
    
    data = pd.DataFrame({
        'ticker': ['AFLT'] * n_samples,
        'begin': pd.date_range('2025-01-01', periods=n_samples),
        'nn_news_sum': np.random.uniform(0.5, 2.0, n_samples),
        'nn_news_mean': np.random.uniform(0.01, 0.05, n_samples),
        'nn_news_max': np.random.uniform(0.1, 0.3, n_samples),
        'nn_news_count': np.random.randint(30, 70, n_samples),
        'sentiment_mean': np.random.uniform(0.3, 0.7, n_samples),
        'sentiment_sum': np.random.uniform(10, 30, n_samples),
        'sentiment_count': np.random.randint(30, 70, n_samples),
        'sentiment_positive_count': np.random.randint(10, 40, n_samples),
        'sentiment_negative_count': np.random.randint(5, 20, n_samples),
        'sentiment_neutral_count': np.random.randint(5, 20, n_samples),
        'rsi': np.random.uniform(20, 80, n_samples),
        'macd': np.random.uniform(-2, 2, n_samples),
        'cci': np.random.uniform(-100, 100, n_samples),
        'ema9': np.random.uniform(80, 120, n_samples),
        'ema50': np.random.uniform(80, 120, n_samples),
        'areThreeWhiteSoldiers': np.random.randint(0, 2, n_samples),
        'areThreeBlackCrows': np.random.randint(0, 2, n_samples),
        'doji': np.random.randint(0, 2, n_samples),
        'bearishEngulfing': np.random.randint(0, 2, n_samples),
        'bullishEngulfing': np.random.randint(0, 2, n_samples),
        'open': np.random.uniform(80, 120, n_samples),
        'high': np.random.uniform(85, 125, n_samples),
        'low': np.random.uniform(75, 115, n_samples),
        'close': np.random.uniform(80, 120, n_samples),
        'volume': np.random.randint(500000, 2000000, n_samples)
    })
    
    return data

def test_new_endpoints():
    """Тестирование новых эндпоинтов"""
    base_url = "http://localhost:8009"
    
    print("=== Тестирование новых эндпоинтов ===\n")
    
    # 1. Получаем конфигурацию по умолчанию
    print("1. Получение конфигурации по умолчанию:")
    try:
        response = requests.get(f"{base_url}/training-config")
        if response.status_code == 200:
            config = response.json()
            print(f"   Статус: {response.status_code}")
            print(f"   Конфигурация: {json.dumps(config['default_config'], indent=2)}")
        else:
            print(f"   Ошибка: {response.status_code}")
    except Exception as e:
        print(f"   Ошибка: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 2. Создаем и загружаем тестовые данные
    print("2. Создание и загрузка тестовых данных:")
    try:
        # Создаем тестовые данные
        test_data = create_test_data()
        test_data.to_csv("test_data.csv", index=False)
        
        # Загружаем файл
        with open("test_data.csv", "rb") as f:
            files = {"file": ("test_data.csv", f, "text/csv")}
            response = requests.post(f"{base_url}/upload-data", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Статус: {response.status_code}")
            print(f"   Файл: {result['filename']}")
            print(f"   Строк: {result['rows_count']}")
            print(f"   Колонок: {result['columns_count']}")
        else:
            print(f"   Ошибка: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   Ошибка: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 3. Получаем список файлов
    print("3. Получение списка загруженных файлов:")
    try:
        response = requests.get(f"{base_url}/data-files")
        if response.status_code == 200:
            result = response.json()
            print(f"   Статус: {response.status_code}")
            print(f"   Файлы: {result['files']}")
        else:
            print(f"   Ошибка: {response.status_code}")
    except Exception as e:
        print(f"   Ошибка: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 4. Обучаем модель с настраиваемыми параметрами
    print("4. Обучение модели с настраиваемыми параметрами:")
    try:
        # Конфигурация для обучения
        training_config = {
            "train_size": 30,
            "test_size": 20,
            "rf_n_estimators": 100,
            "rf_max_depth": 10,
            "gb_n_estimators": 100,
            "gb_learning_rate": 0.05,
            "ensemble_weights": [2, 2, 1, 1, 1],
            "cv_splits": 3
        }
        
        data = {
            "filename": "test_data.csv",
            "config": json.dumps(training_config)
        }
        
        response = requests.post(f"{base_url}/train", data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Статус: {response.status_code}")
            print(f"   Сообщение: {result['message']}")
            print(f"   Обученные модели: {result['models_trained']}")
            print(f"   Всего признаков: {result['feature_count']}")
            print(f"   Отобрано признаков: {result['selected_features_count']}")
            print(f"   Метрики обучения:")
            for target, metrics in result['training_metrics'].items():
                print(f"     {target}: CV MAE = {metrics['cv_mae_mean']:.4f} (+/- {metrics['cv_mae_std']:.4f})")
        else:
            print(f"   Ошибка: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   Ошибка: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 5. Проверяем статус после обучения
    print("5. Проверка статуса после обучения:")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            result = response.json()
            print(f"   Статус: {response.status_code}")
            print(f"   Загружено моделей: {result['models_loaded']}")
            print(f"   Доступные цели: {result['available_targets']}")
        else:
            print(f"   Ошибка: {response.status_code}")
    except Exception as e:
        print(f"   Ошибка: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 6. Тестируем предсказание с новыми моделями
    print("6. Тестирование предсказания с новыми моделями:")
    try:
        test_prediction_data = {
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
                }
            ]
        }
        
        response = requests.post(
            f"{base_url}/predict",
            headers={"Content-Type": "application/json"},
            json=test_prediction_data
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Статус: {response.status_code}")
            print(f"   Количество предсказанных свечей: {len(result['predictions'])}")
            print(f"   Первая свеча: {result['predictions'][0]}")
        else:
            print(f"   Ошибка: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   Ошибка: {e}")
    
    print("\n=== Тестирование завершено ===")

if __name__ == "__main__":
    test_new_endpoints()
