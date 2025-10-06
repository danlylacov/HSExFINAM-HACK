import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_sample_data(filename="sample_stock_data.csv", n_days=100):
    """
    Создание примера данных для обучения модели
    
    Args:
        filename: имя файла для сохранения
        n_days: количество дней данных
    """
    np.random.seed(42)
    
    # Базовые параметры
    base_price = 100.0
    base_volume = 1000000
    
    # Создание дат
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(n_days)]
    
    # Создание данных
    data = []
    
    for i, date in enumerate(dates):
        # Цены с трендом и волатильностью
        trend = 0.001 * i  # небольшой восходящий тренд
        volatility = 0.02 + 0.01 * np.sin(i * 0.1)  # изменяющаяся волатильность
        
        # OHLC цены
        open_price = base_price * (1 + trend + np.random.normal(0, volatility))
        close_price = open_price * (1 + np.random.normal(0, volatility * 0.5))
        high_price = max(open_price, close_price) * (1 + abs(np.random.normal(0, volatility * 0.3)))
        low_price = min(open_price, close_price) * (1 - abs(np.random.normal(0, volatility * 0.3)))
        
        # Объем с корреляцией к волатильности
        volume_multiplier = 1 + volatility * 2
        volume = int(base_volume * volume_multiplier * (1 + np.random.normal(0, 0.2)))
        
        # Новостные данные
        news_count = np.random.randint(20, 80)
        news_sum = np.random.uniform(0.5, 2.5)
        news_mean = news_sum / news_count
        news_max = np.random.uniform(0.1, 0.4)
        
        # Сентимент данные
        sentiment_count = np.random.randint(30, 70)
        sentiment_mean = np.random.uniform(0.3, 0.7)
        sentiment_sum = sentiment_mean * sentiment_count
        
        # Распределение сентимента
        pos_count = int(sentiment_count * np.random.uniform(0.3, 0.6))
        neg_count = int(sentiment_count * np.random.uniform(0.1, 0.3))
        neutral_count = sentiment_count - pos_count - neg_count
        
        # Технические индикаторы
        rsi = np.random.uniform(20, 80)
        macd = np.random.uniform(-2, 2)
        cci = np.random.uniform(-100, 100)
        
        # Скользящие средние
        ema9 = base_price * (1 + trend + np.random.normal(0, volatility * 0.5))
        ema50 = base_price * (1 + trend + np.random.normal(0, volatility * 0.3))
        
        # Свечные паттерны (редко встречающиеся)
        patterns = {
            'areThreeWhiteSoldiers': 1 if np.random.random() < 0.05 else 0,
            'areThreeBlackCrows': 1 if np.random.random() < 0.05 else 0,
            'doji': 1 if np.random.random() < 0.1 else 0,
            'bearishEngulfing': 1 if np.random.random() < 0.05 else 0,
            'bullishEngulfing': 1 if np.random.random() < 0.05 else 0
        }
        
        row = {
            'ticker': 'SAMPLE',
            'begin': date.strftime('%Y-%m-%d'),
            'nn_news_sum': round(news_sum, 3),
            'nn_news_mean': round(news_mean, 4),
            'nn_news_max': round(news_max, 3),
            'nn_news_count': news_count,
            'sentiment_mean': round(sentiment_mean, 3),
            'sentiment_sum': round(sentiment_sum, 1),
            'sentiment_count': sentiment_count,
            'sentiment_positive_count': pos_count,
            'sentiment_negative_count': neg_count,
            'sentiment_neutral_count': neutral_count,
            'rsi': round(rsi, 1),
            'macd': round(macd, 3),
            'cci': round(cci, 1),
            'ema9': round(ema9, 2),
            'ema50': round(ema50, 2),
            'areThreeWhiteSoldiers': patterns['areThreeWhiteSoldiers'],
            'areThreeBlackCrows': patterns['areThreeBlackCrows'],
            'doji': patterns['doji'],
            'bearishEngulfing': patterns['bearishEngulfing'],
            'bullishEngulfing': patterns['bullishEngulfing'],
            'open': round(open_price, 2),
            'high': round(high_price, 2),
            'low': round(low_price, 2),
            'close': round(close_price, 2),
            'volume': volume
        }
        
        data.append(row)
    
    # Создание DataFrame
    df = pd.DataFrame(data)
    
    # Сохранение в CSV
    df.to_csv(filename, index=False)
    
    print(f"✅ Создан файл {filename}")
    print(f"   Строк: {len(df)}")
    print(f"   Колонок: {len(df.columns)}")
    print(f"   Период: {df['begin'].min()} - {df['begin'].max()}")
    print(f"   Цены: {df['open'].min():.2f} - {df['open'].max():.2f}")
    print(f"   Объемы: {df['volume'].min():,} - {df['volume'].max():,}")
    
    return df

def create_multiple_tickers(filename="multi_ticker_data.csv", tickers=['AFLT', 'SBER', 'GAZP'], days_per_ticker=50):
    """
    Создание данных для нескольких тикеров
    """
    all_data = []
    
    for ticker in tickers:
        print(f"Создание данных для {ticker}...")
        ticker_data = create_sample_data(f"temp_{ticker}.csv", days_per_ticker)
        ticker_data['ticker'] = ticker
        all_data.append(ticker_data)
    
    # Объединение данных
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Сортировка по дате
    combined_df = combined_df.sort_values(['ticker', 'begin']).reset_index(drop=True)
    
    # Сохранение
    combined_df.to_csv(filename, index=False)
    
    print(f"\n✅ Создан файл {filename}")
    print(f"   Тикеров: {len(tickers)}")
    print(f"   Общее количество строк: {len(combined_df)}")
    print(f"   Колонок: {len(combined_df.columns)}")
    
    # Удаление временных файлов
    for ticker in tickers:
        import os
        os.remove(f"temp_{ticker}.csv")
    
    return combined_df

if __name__ == "__main__":
    print("=== Генератор примеров данных для обучения ===")
    print()
    
    # Создание простого примера
    print("1. Создание простого примера (100 дней):")
    create_sample_data("sample_data.csv", 100)
    
    print("\n" + "="*50 + "\n")
    
    # Создание расширенного примера
    print("2. Создание расширенного примера (200 дней):")
    create_sample_data("extended_sample_data.csv", 200)
    
    print("\n" + "="*50 + "\n")
    
    # Создание мульти-тикер примера
    print("3. Создание мульти-тикер примера:")
    create_multiple_tickers("multi_ticker_data.csv", ['AFLT', 'SBER', 'GAZP'], 60)
    
    print("\n🎉 Все примеры данных созданы!")
    print("\n📋 Созданные файлы:")
    print("   - sample_data.csv (100 дней, 1 тикер)")
    print("   - extended_sample_data.csv (200 дней, 1 тикер)")
    print("   - multi_ticker_data.csv (60 дней, 3 тикера)")
    print("\n🚀 Использование:")
    print("   python3 quick_train.sh sample_data.csv")
