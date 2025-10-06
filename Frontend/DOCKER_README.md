# 🐳 Docker Setup Complete!

## Быстрый старт

### 1. Production (рекомендуется)
```bash
# Сборка и запуск
make prod
# или
./docker.sh prod

# Приложение: http://localhost:3000
```

### 2. Development
```bash
# Запуск с hot reload
make dev
# или
./docker.sh dev

# Приложение: http://localhost:5173
```

## 📋 Доступные команды

| Команда | Описание |
|---------|----------|
| `make build` | Сборка production образа |
| `make dev` | Development сервер |
| `make prod` | Production сервер |
| `make stop` | Остановка контейнеров |
| `make logs` | Просмотр логов |
| `make health` | Проверка здоровья |
| `make clean` | Очистка Docker |

## 🔧 Что включено

- ✅ **Multi-stage build** - оптимизированный размер образа
- ✅ **Nginx** - production веб-сервер с SPA поддержкой
- ✅ **Health checks** - мониторинг состояния
- ✅ **Gzip compression** - сжатие статических файлов
- ✅ **Security headers** - базовые заголовки безопасности
- ✅ **Development mode** - hot reload для разработки

## 📁 Созданные файлы

- `Dockerfile` - Production сборка
- `Dockerfile.dev` - Development сборка  
- `docker-compose.yml` - Orchestration
- `nginx.conf` - Nginx конфигурация
- `.dockerignore` - Исключения для сборки
- `docker.sh` - Скрипт управления
- `Makefile` - Удобные команды
- `DOCKER.md` - Подробная документация

## 🚀 Готово к деплою!

Образ готов для развертывания в любой Docker-совместимой среде.
