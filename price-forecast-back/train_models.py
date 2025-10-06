import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor, ExtraTreesRegressor
from sklearn.linear_model import Ridge, Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
import warnings
warnings.filterwarnings('ignore')

def json_to_dataframe_simple(json_file):
    df = pd.read_json(json_file)
    return df

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

def train_and_save_models():
    """Обучение и сохранение моделей"""
    
    # Загружаем данные (адаптируем под ваши файлы)
    try:
        data = pd.read_csv('итог2.csv')
        data2 = json_to_dataframe_simple('response.json')
        data2 = data2[:50]
        result = pd.concat([data, data2], axis=1)
    except FileNotFoundError as e:
        print(f"Файл не найден: {e}")
        print("Создаем тестовые данные...")
        
        # Создаем тестовые данные для демонстрации
        np.random.seed(42)
        n_samples = 50
        
        result = pd.DataFrame({
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
    
    # Разделяем данные
    train_df = result[:25]
    test_df = result[25:]
    
    # Преобразование дат
    train_df['begin'] = pd.to_datetime(train_df['begin'])
    test_df['begin'] = pd.to_datetime(test_df['begin'])
    
    # Сортировка по дате
    train_df = train_df.sort_values('begin')
    test_df = test_df.sort_values('begin')
    
    # Создание дополнительных признаков
    print("Создание дополнительных признаков...")
    train_df = create_features(train_df)
    test_df = create_features(test_df)
    
    # Заполнение пропусков
    train_df = train_df.bfill().ffill()
    test_df = test_df.bfill().ffill()
    
    # Целевые переменные
    target_columns = ['open', 'high', 'low', 'close', 'volume']
    
    # Автоматическое определение ЧИСЛОВЫХ признаков
    exclude_columns = ['ticker', 'begin'] + target_columns
    
    # Выбираем только числовые колонки
    numeric_columns = train_df.select_dtypes(include=[np.number]).columns.tolist()
    feature_columns = [col for col in numeric_columns if col not in exclude_columns]
    
    print(f"Всего числовых признаков: {len(feature_columns)}")
    print(f"Первые 10 признаков: {feature_columns[:10]}")
    
    # Создаем папку для моделей
    os.makedirs('models', exist_ok=True)
    
    # Улучшенный ансамбль для каждой целевой переменной
    ensemble_models = {}
    scalers = {}
    feature_selectors = {}
    
    for target in target_columns:
        print(f"\nСоздание улучшенного ансамбля для {target}...")
        
        # Подготовка данных - используем ТОЛЬКО числовые признаки
        X_train = train_df[feature_columns]
        y_train = train_df[target]
        X_test = test_df[feature_columns]
        
        # Проверяем на пропуски
        print(f"Пропуски в X_train: {X_train.isnull().sum().sum()}")
        print(f"Пропуски в y_train: {y_train.isnull().sum()}")
        
        # Удаляем строки с пропусками в целевой переменной
        valid_indices = ~y_train.isnull()
        X_train = X_train[valid_indices]
        y_train = y_train[valid_indices]
        
        # Масштабирование
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        scalers[target] = scaler
        
        # Отбор признаков с помощью RandomForest
        selector = SelectFromModel(
            RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1),
            threshold='median'
        )
        X_train_selected = selector.fit_transform(X_train_scaled, y_train)
        X_test_selected = selector.transform(X_test_scaled)
        feature_selectors[target] = selector
        
        print(f"Отобрано {X_train_selected.shape[1]} признаков из {X_train_scaled.shape[1]}")
        
        # Разнообразные базовые модели
        models = [
            ('rf', RandomForestRegressor(
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )),
            ('gb', GradientBoostingRegressor(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=6,
                min_samples_split=5,
                random_state=42
            )),
            ('et', ExtraTreesRegressor(
                n_estimators=150,
                max_depth=15,
                min_samples_split=5,
                random_state=42,
                n_jobs=-1
            )),
            ('ridge', Ridge(alpha=1.0, random_state=42)),
            ('lasso', Lasso(alpha=0.1, random_state=42, max_iter=2000))
        ]
        
        # Ансамбль с весами
        ensemble = VotingRegressor(
            estimators=models,
            weights=[3, 3, 2, 1, 1]  # Веса для моделей
        )
        
        # Кросс-валидация
        tscv = TimeSeriesSplit(n_splits=5)
        cv_scores = cross_val_score(ensemble, X_train_selected, y_train, 
                                   cv=tscv, scoring='neg_mean_absolute_error')
        print(f"CV MAE: {-cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        # Обучение
        ensemble.fit(X_train_selected, y_train)
        
        # Предсказание
        pred = ensemble.predict(X_test_selected)
        
        # Сохранение модели
        ensemble_models[target] = ensemble
        
        # Сохраняем модели
        joblib.dump(ensemble, f'models/{target}_model.pkl')
        joblib.dump(scaler, f'models/{target}_scaler.pkl')
        joblib.dump(selector, f'models/{target}_selector.pkl')
        
        print(f"Модель для {target} сохранена")
    
    # Сохраняем список признаков
    joblib.dump(feature_columns, 'models/feature_columns.pkl')
    
    print(f"\nВсе модели сохранены в папку 'models'")
    print(f"Сохранено {len(ensemble_models)} моделей")
    
    return ensemble_models, scalers, feature_selectors, feature_columns

if __name__ == "__main__":
    train_and_save_models()
