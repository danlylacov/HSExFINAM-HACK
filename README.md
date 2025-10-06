# HSExFINAM-HACK
Платформа для анализа финансовых рынков и краткосрочного прогнозирования цен, объединяющая технический анализ временных рядов и влияние новостного фона. Состоит из набора микросервисов (NLP по новостям, технические индикаторы, агрегатор данных и сервис прогноза) и фронтенда для визуализации графиков, метрик и результатов инференса.

__Решение кейса Forecast__ - прогнозирование котировок акций на основе временных рядов и новостей [__на хакатоне HSExFINAM HACK__](https://broker.finam.ru/landing/finam-ai-trade-hack/) (3/10/25 - 5/10/25)

__Команда Back2Back__

__Состав:__
- Лулаков Даниил - Dev-ops, Fullstack, ML
- Гезенцвей Виктор - Back-end
- Беляев Валенрий - ML
 - Сорокина Апполинария - ML


__Презентация:__  [click](https://github.com/danlylacov/HSExFINAM-HACK/blob/main/finam-hack.pdf)


### Обзор монорепозитория
В репозитории собраны 4 сервиса и фронтенд-приложение:
- `Frontend/` — SPA интерфейс для визуализации котировок, новостей и прогнозов.
- `collector-of-all-data/` — Java Spring Boot сервис-агрегатор данных (REST/WebFlux/WebSocket).
- `market-analyzer-service/` — Java Spring Boot сервис технического анализа и индикаторов.
- `news_analise_final/` — Python FastAPI сервис анализа новостей и извлечения фич (NLP/NN).
- `price-forecast-back/` — Python FastAPI сервис прогноза цен на основе ансамбля ML-моделей.

### Архитектура (высокоуровнево)
- Фронтенд запрашивает данные и прогнозы от бэкендов, отображает графики и метрики.
- `collector-of-all-data` может выступать шлюзом-агрегатором для данных рынков и новостей, с возможностью реактивной доставки через WebFlux/WebSocket.
- `market-analyzer-service` рассчитывает технические индикаторы и паттерны по свечным данным.
- `news_analise_final` классифицирует и агрегирует новостные события в числовые фичи (в т.ч. с затуханием по времени).
- `price-forecast-back` объединяет фичи (тех. индикаторы + новости) и выдает прогнозы будущих свечей.

---

### Frontend (`Frontend/`)
- Технологии: React 18, TypeScript, Vite 7, Tailwind CSS, React Router, Lightweight Charts, Framer Motion, Lucide Icons.
- Сборка/запуск: `npm run dev` (локально), прод через Nginx (Docker multi-stage).
- Порт: 80 (в контейнере Nginx).
- Особенности реализации:
  - Современная темная тема, адаптивный UI, плавные анимации.
  - Компонентная архитектура, типизация TS, быстрый дев-сервер Vite.
  - Графики котировок и отображение новостей/метрик.

### Market Analyzer Service (`market-analyzer-service/`)
- Технологии: Java 21, Spring Boot 3.5, TA4J (тех. анализ), OpenCSV, Springdoc OpenAPI.
- Сборка: Maven, JAR + Docker multi-stage; порт 8081.
- Особенности реализации:
  - Расчет индикаторов (RSI, MACD и др.) и свечных паттернов на основе TA4J.
  - REST API с автогенерацией Swagger UI через springdoc.
  - Импорт CSV данных через OpenCSV.

### Data Collector / Aggregator (`collector-of-all-data/`)
- Технологии: Java 21, Spring Boot 3.5, WebFlux, WebSocket, Springdoc OpenAPI.
- Сборка: Maven, JAR + Docker multi-stage; порт 8087.
- Особенности реализации:
  - Реактивная обработка потоков данных (WebFlux).
  - Возможность вещания обновлений через WebSocket.
  - REST API и Swagger UI; удобен как шлюз-агрегатор между сервисами.

### News Analysis Service (`news_analise_final/`)
- Технологии: Python 3.10, FastAPI, PyTorch, scikit-learn, pandas, numpy, pyarrow; NLP для русского языка (razdel, pymorphy3, rapidfuzz, emoji).
- Запуск: Uvicorn; порт 8000. Dockerfile и docker-compose в `config/`.
- Основные возможности:
  - Классификация релевантности новостей по тикерам; агрегация новостных фич с учетом полураспада.
  - REST API (`/infer`, `/health`), Swagger UI (`/docs`).
  - Поддержка файловых и JSON запросов; артефакты модели в `artifacts/`.

### Price Forecast Backend (`price-forecast-back/`)
- Технологии: Python FastAPI, scikit-learn (ансамбль: RandomForest, GradientBoosting, ExtraTrees, Ridge, Lasso), pandas, numpy.
- Порт: 8009. Возможности обучения и инференса.
- Основные эндпоинты:
  - `POST /predict` — прогноз следующих 20 свечей на основании исторических данных и фич.
  - `POST /upload-data`, `POST /train`, `GET /training-config`, `GET /data-files`, `GET /health`.
- Особенности реализации:
  - Пайплайн признаков: новостные фичи (`nn_news_*`, `sentiment_*`), тех. индикаторы (RSI, MACD, CCI, EMA9/50), свечные паттерны.
  - Ансамбль из 5 моделей со взвешенным объединением предсказаний.

---

### Сборка и контейнеризация
- Для каждого сервиса предусмотрены Dockerfile'ы (multi-stage для Java и Frontend):
  - Frontend → Nginx (порт 80)
  - market-analyzer-service → Java JRE (порт 8081)
  - collector-of-all-data → Java JRE (порт 8087)
  - news_analise_final → Uvicorn/FastAPI (порт 8000)
  - price-forecast-back → Python FastAPI (порт 8009)


### Лицензии и документация
- У каждого сервиса есть локальная документация/README. Swagger UI доступен для сервисов на Spring Boot и FastAPI.
