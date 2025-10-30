import os
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor, ExtraTreesRegressor
from sklearn.linear_model import Ridge, Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from fastapi import HTTPException
from typing import Dict, Any, List

from backend_api.models.schemas import TrainingConfig, TrainingResponse
from backend_api.utils.features import create_features

# Глобальные переменные (stateful!)
ensemble_models = {}
scalers = {}
feature_selectors = {}
feature_columns = []
target_columns = ['open', 'high', 'low', 'close', 'volume']

def train_models_with_config(data_file: str, config: TrainingConfig) -> TrainingResponse:
    try:
        if data_file.endswith('.csv'):
            data = pd.read_csv(data_file)
        elif data_file.endswith('.json'):
            data = pd.read_json(data_file)
        else:
            raise ValueError("Неподдерживаемый формат файла")
        if config.test_size is None:
            train_df = data[:config.train_size]
            test_df = data[config.train_size:]
        else:
            train_df = data[:config.train_size]
            test_df = data[config.train_size:config.train_size + config.test_size]
        if 'begin' in train_df.columns:
            train_df['begin'] = pd.to_datetime(train_df['begin'])
            test_df['begin'] = pd.to_datetime(test_df['begin'])
            train_df = train_df.sort_values('begin')
            test_df = test_df.sort_values('begin')
        train_df = create_features(train_df)
        test_df = create_features(test_df)
        train_df = train_df.bfill().ffill().fillna(0)
        test_df = test_df.bfill().ffill().fillna(0)
        exclude_columns = ['ticker', 'begin'] + target_columns
        numeric_columns = train_df.select_dtypes(include=[np.number]).columns.tolist()
        global feature_columns
        feature_columns = [col for col in numeric_columns if col not in exclude_columns]

        os.makedirs('models', exist_ok=True)
        global ensemble_models, scalers, feature_selectors
        ensemble_models = {}
        scalers = {}
        feature_selectors = {}
        training_metrics = {}
        for target in target_columns:
            print(f"Обучение модели для {target}...")
            X_train = train_df[feature_columns]
            y_train = train_df[target]
            X_test = test_df[feature_columns]
            valid_indices = ~y_train.isnull()
            X_train = X_train[valid_indices]
            y_train = y_train[valid_indices]
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            scalers[target] = scaler
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
            ensemble = VotingRegressor(
                estimators=models,
                weights=config.ensemble_weights
            )
            tscv = TimeSeriesSplit(n_splits=config.cv_splits)
            cv_scores = cross_val_score(ensemble, X_train_selected, y_train, cv=tscv, scoring='neg_mean_absolute_error')
            ensemble.fit(X_train_selected, y_train)
            pred = ensemble.predict(X_test_selected)
            ensemble_models[target] = ensemble
            joblib.dump(ensemble, f'models/{target}_model.pkl')
            joblib.dump(scaler, f'models/{target}_scaler.pkl')
            joblib.dump(selector, f'models/{target}_selector.pkl')
            training_metrics[target] = {
                'cv_mae_mean': -cv_scores.mean(),
                'cv_mae_std': cv_scores.std(),
                'selected_features': X_train_selected.shape[1],
                'total_features': X_train_scaled.shape[1]
            }
            print(f"Модель для {target} обучена. CV MAE: {-cv_scores.mean():.4f}")
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

def load_models() -> bool:
    global ensemble_models, scalers, feature_selectors, feature_columns
    try:
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
    try:
        df = pd.DataFrame([input_data])
        df = create_features(df)
        df = df.bfill().ffill().fillna(0)
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        exclude_columns = ['ticker', 'begin'] + target_columns
        current_feature_columns = [col for col in numeric_columns if col not in exclude_columns]
        X = df[current_feature_columns]
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
