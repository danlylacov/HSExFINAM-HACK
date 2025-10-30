import pandas as pd

def create_features(df: pd.DataFrame) -> pd.DataFrame:
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
    if all(col in df.columns for col in ['high', 'low', 'open']):
        df['volatility'] = (df['high'] - df['low']) / df['open']
    # Взаимодействия признаков
    if all(col in df.columns for col in ['rsi', 'macd']):
        df['rsi_macd_interaction'] = df['rsi'] * df['macd']
    return df
