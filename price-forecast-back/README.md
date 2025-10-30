# Price Forecast Backend

## Cтруктура проекта

```
price-forecast-back/
├── backend_api/
│   ├── main_v1.py           # Главный FastAPI backend (v1)
│   └── main_v2.py           # FastAPI backend optimized (v2)
├── ml_core/                 # В будущем ML-функции, утилиты, пайплайны
├── requirements.txt         # Зависимости Python
├── Dockerfile               # Docker сборка backend
├── docker-compose.yml       # Docker orchestration
├── nginx.conf               # (Опционально) Прокси/Nginx
├── models/                  # Обученные модели (pkl)
├── data/                    # Данные для обучения/предсказания
└── README.md                # Этот файл
```

## Быстрый старт

### Локально (Python 3.10+)
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python backend_api/main_v1.py
# или (экспериментальный)
python backend_api/main_v2.py
```

### Docker (рекомендовано)
```bash
docker-compose up --build
```

Бэкенд будет доступен на [http://localhost:8009](http://localhost:8009)

## Основные Endpoints (FastAPI, v1/v2)
- `/` – Статус API
- `/health` – Лоадер моделей, статус работы backend
- `/upload-data` [POST] – Загрузка пользовательских данных (`.csv`/`.json`)
- `/train` [POST] – Обучение моделей (принимает имя файла и JSON-конфиг)
- `/predict` [POST] – Предсказание доходности, формат input (JSON, свечи)
- `/process-combined-data` [POST] – Комбинированный endpoint с callback (интеграция для внешних платформ)
- `/training-config` [GET] – Справка по параметрам обучения
- `/data-files` [GET] – Доступные пользовательские датасеты

Полный OpenAPI docs: http://localhost:8009/docs

## Описание данных
- **Вход:** Последовательность исторических свечей со всеми признаками, включая расчетные (rsi, macd, sentiment & news features).
- **Выход:** Доходности или значения свечей на заданный горизонт (обычно p1..p20 – доходности на 20 свечей вперёд).

## Как обучить/долучить модель
1. Загрузите пользовательский датасет через `/upload-data`.
2. Запустите `/train` с указанием имени файла и конфигурации (см. `/training-config` для шаблона параметров).
3. После успешного обучения модели автоматически обновляются в API.

## Cистема/Модули
- **backend_api/** – API-ендпоинты и сервисная FastAPI логика (отдельные версии backend)
- **ml_core/** – Для ML-логики, датасетов, фиче-инженирингу и утилит (рекомендуется выносить энкодеры, препроцессоры, пайплайны)
- **models/** – Только .pkl артефакты моделей и препроцессоров
- **data/** – Пользовательские и тестовые данные (csv/json, без артефактных файлов)

## Рекомендации по коммитам и CI/CD
- Не хранить артефакты, pycache, ни один csv/json кроме необходимых
- Все тесты, временные/notebook-файлы и скрипты: внести в /tests или не хранить вовсе
- Документация по API – только в этом README или автогенерируемом OpenAPI

---

© Senior Level Structuring by request. Вопросы по вёрстке, структуре и CI/CD — к авторам и ревьюерам проекта.
