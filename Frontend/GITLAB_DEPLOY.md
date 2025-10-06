# 🚀 GitLab Deployment Guide

## 📋 Подготовка к деплою

### 1. Создание проекта в GitLab

1. Войдите в GitLab
2. Нажмите "New Project" → "Create blank project"
3. Заполните:
   - **Project name**: `finam-frontend`
   - **Project URL**: выберите группу/пользователя
   - **Visibility Level**: Private/Internal/Public (по выбору)

### 2. Настройка Container Registry

GitLab автоматически предоставляет Container Registry для каждого проекта.

**Registry URL**: `registry.gitlab.com/your-group/finam-frontend`

### 3. Настройка переменных окружения

В GitLab перейдите в **Settings** → **CI/CD** → **Variables** и добавьте:

| Variable | Value | Description |
|----------|-------|-------------|
| `DOCKER_REGISTRY` | `registry.gitlab.com` | GitLab Container Registry |
| `PRODUCTION_URL` | `https://yourdomain.com` | Production URL |
| `STAGING_URL` | `https://staging.yourdomain.com` | Staging URL |

## 🔧 Локальная настройка

### 1. Инициализация Git репозитория

```bash
# Если еще не инициализирован
git init

# Добавить GitLab remote
git remote add origin git@gitlab.com:your-group/finam-frontend.git

# Или через HTTPS
git remote add origin https://gitlab.com/your-group/finam-frontend.git
```

### 2. Создание .gitignore

```bash
# Создать .gitignore если его нет
cat > .gitignore << 'EOF'
# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build outputs
dist/
build/

# Environment files
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Logs
logs/
*.log

# Coverage directory
coverage/

# Temporary folders
tmp/
temp/
EOF
```

## 📤 Первый деплой

### 1. Коммит и пуш

```bash
# Добавить все файлы
git add .

# Создать коммит
git commit -m "Initial commit: FINAM Frontend with Docker"

# Отправить в GitLab
git push -u origin main
```

### 2. Проверка CI/CD

1. Перейдите в **CI/CD** → **Pipelines**
2. Убедитесь, что pipeline запустился
3. Проверьте, что все этапы прошли успешно:
   - ✅ **build** - сборка Docker образа
   - ✅ **test** - тесты и линтер
   - ✅ **deploy_staging** - деплой на staging (для develop ветки)

## 🌐 Настройка доменов

### 1. Staging Environment

```bash
# Пример команды для деплоя на staging сервер
docker run -d \
  --name finam-frontend-staging \
  -p 3001:80 \
  registry.gitlab.com/your-group/finam-frontend:latest
```

### 2. Production Environment

```bash
# Пример команды для деплоя на production сервер
docker run -d \
  --name finam-frontend-production \
  -p 80:80 \
  -p 443:443 \
  registry.gitlab.com/your-group/finam-frontend:latest
```

## 🔄 Workflow

### Development Workflow

```bash
# 1. Создать feature ветку
git checkout -b feature/new-feature

# 2. Внести изменения
# ... код ...

# 3. Коммит и пуш
git add .
git commit -m "Add new feature"
git push origin feature/new-feature

# 4. Создать Merge Request в GitLab
# 5. После одобрения - merge в develop
```

### Production Deployment

```bash
# 1. Merge develop в main
git checkout main
git merge develop
git push origin main

# 2. В GitLab перейти в CI/CD → Pipelines
# 3. Нажать "Deploy to Production" (manual trigger)
```

## 🐳 Docker Registry Commands

### Локальная работа с Registry

```bash
# Логин в GitLab Container Registry
docker login registry.gitlab.com

# Pull образа
docker pull registry.gitlab.com/your-group/finam-frontend:latest

# Запуск локально
docker run -p 3000:80 registry.gitlab.com/your-group/finam-frontend:latest
```

### Тегирование версий

```bash
# Создать тег для релиза
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# В GitLab CI/CD будет создан образ с тегом v1.0.0
```

## 🔧 Настройка серверов

### 1. Staging Server

```bash
# На staging сервере
docker pull registry.gitlab.com/your-group/finam-frontend:latest
docker stop finam-frontend-staging || true
docker rm finam-frontend-staging || true
docker run -d \
  --name finam-frontend-staging \
  --restart unless-stopped \
  -p 3001:80 \
  registry.gitlab.com/your-group/finam-frontend:latest
```

### 2. Production Server

```bash
# На production сервере
docker pull registry.gitlab.com/your-group/finam-frontend:latest
docker stop finam-frontend-production || true
docker rm finam-frontend-production || true
docker run -d \
  --name finam-frontend-production \
  --restart unless-stopped \
  -p 80:80 \
  -p 443:443 \
  registry.gitlab.com/your-group/finam-frontend:latest
```

## 📊 Мониторинг

### Health Checks

```bash
# Проверка staging
curl https://staging.yourdomain.com/health

# Проверка production
curl https://yourdomain.com/health
```

### Логи

```bash
# Просмотр логов контейнера
docker logs finam-frontend-production

# Следить за логами в реальном времени
docker logs -f finam-frontend-production
```

## 🚨 Troubleshooting

### Проблемы с Registry

```bash
# Очистка локального кэша Docker
docker system prune -a

# Перелогин в Registry
docker logout registry.gitlab.com
docker login registry.gitlab.com
```

### Проблемы с Pipeline

1. Проверьте переменные окружения в GitLab
2. Убедитесь, что Container Registry включен
3. Проверьте права доступа к проекту

### Проблемы с деплоем

```bash
# Проверка статуса контейнера
docker ps -a

# Проверка логов
docker logs finam-frontend-production

# Перезапуск контейнера
docker restart finam-frontend-production
```

## 📈 Дополнительные возможности

### 1. Автоматические деплои

Настройте webhook для автоматического деплоя при успешном pipeline.

### 2. Rollback

```bash
# Откат к предыдущей версии
docker run -d \
  --name finam-frontend-production \
  registry.gitlab.com/your-group/finam-frontend:previous-tag
```

### 3. Blue-Green Deployment

Настройте blue-green deployment для zero-downtime обновлений.

---

## 🎯 Готово к деплою!

Ваш проект готов для деплоя в GitLab. Следуйте инструкциям выше для настройки и деплоя.
