# Notes Backend API

Backend API для приложения заметок.
Поддерживает аутентификацию пользователей, CRUD-операции для заметок, изоляцию данных по пользователям и построен по слоистой архитектуре.

Проект учебный с акцентом на best practices для учебных и pet-проектов.


## Features

- Аутентификация пользователей с изоляцией данных
- CRUD-операции для заметок
- Доступ к данным строго в рамках текущего пользователя
- Слоистая архитектура (routes / services / repositories)
- Централизованная обработка ошибок и кастомные исключения
- Валидация входных и выходных данных через Pydantic
- Работа с БД через SQLAlchemy (отсутствие «сырого» SQL в логике)
- Контейнеризация с Docker и Docker Compose
- CI: автоматический запуск тестов при каждом push
- Автогенерируемая OpenAPI-документация (Swagger UI)


## Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy
- Pydantic v2
- PostgreSQL
- Alembic
- Docker, Docker Compose
- Pytest
- GitHub Actions


## Architecture

Проект построен по слоистой архитектуре:
- API layer — HTTP endpoints
- Service layer — бизнес-логика
- Repository layer — работа с БД
- Models / Schemas — ORM и Pydantic модели

Слои изолированы и не зависят напрямую друг от друга.


## Tests

Проект покрыт юнит и интеграционными тестами с использованием Pytest и FastAPI TestClient.

Примеры проверяемых сценариев:
- CRUD операции для заметок (create, read, update, delete)
- Авторизация и аутентификация пользователей
- Проверка валидации данных
- Обработка ошибок (например, доступ запрещён, заметка не найдена)


## Project Structure
```text
app/
 ├─ core/         # Конфигурация, настройки (pydantic-settings)
 ├─ dependencies/ # Зависимости FastAPI (get_db, get_current_user)
 ├─ exceptions/   # Кастомные ошибки и обработчики
 ├─ models/       # SQLAlchemy модели (DB Schema)
 ├─ repositories/ # Прямая работа с БД
 ├─ routes/       # Контроллеры / Эндпоинты
 ├─ schemas/      # Pydantic модели (DTO)
 ├─ services/     # Бизнес-логика (связующее звено)
 └─ main.py       # Точка входа в приложение
```

## API Endpoints

Auth:
- POST /auth/register
- POST /auth/login
- POST /auth/logout

Notes:
- GET /notes/
- GET /notes/{note_id}
- POST /notes/
- PATCH /notes/{note_id}
- DELETE /notes/{note_id}


# Getting Started

## Environment Variables

Создайте файл .env на основе примера:
`.env.example `

Note: Не забудьте обновить DATABASE_URL и секретные ключи в .env.


## Run with Docker (Recommended)

`docker-compose up --build`


## Local Development
```bash
# Установка зависимостей
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt

# Применение миграций
alembic upgrade head

# Запуск сервера
uvicorn app.main:app --reload
```
# Development & Testing

- Запуск тестов: `python -m pytest`
- Создание миграции: `alembic revision --autogenerate -m "description"`
- Применение миграций: `alembic upgrade head`
- Интерактивная документация: После запуска доступна по адресу http://localhost:8000/docs (Swagger UI).


# Author
Исхаков Расул