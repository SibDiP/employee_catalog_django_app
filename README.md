# Online Employees Catalog

Каталог сотрудников компании с иерархической структурой (дерево «руководитель → подчинённые»).
Проект состоит из двух приложений, работающих с одной и той же базой данных:

- **Django** — веб-интерфейс каталога, админка, миграции и запись данных в дерево.
- **FastAPI** — асинхронное REST API (JSON) для чтения сотрудников, поддеревьев и корневых узлов.

---

## 1. Быстрый старт

### Требования

- Python `^3.10` (проверено на 3.12)
- [Poetry](https://python-poetry.org/) 2.x
- PostgreSQL **не обязателен**: по умолчанию используется SQLite

### Установка

Выполнять из корня репозитория:

```bash
poetry install
cp .env_example .env
```

`.env` настроен на SQLite (`USE_SQLITE=True`); для PostgreSQL заполните `DB_*` и выставьте `USE_SQLITE=False`.

### Django (веб-интерфейс)

Все команды Django запускаются из каталога `online_employees_catalog/` — путь к SQLite задан относительно рабочей директории, при запуске из корня создастся пустая БД и API вернёт `500`.

```bash
cd online_employees_catalog
poetry run python manage.py migrate
poetry run python manage.py createsuperuser   # опционально, для /admin/
poetry run python manage.py runserver
```

- Каталог: http://127.0.0.1:8000/
- Админка: http://127.0.0.1:8000/admin/

### FastAPI (REST API)

В отдельном терминале, тоже из `online_employees_catalog/`:

```bash
poetry run uvicorn fastapi_api.main:app --reload --port 8001
```

- Swagger UI: http://127.0.0.1:8001/docs
- Health-check: http://127.0.0.1:8001/health

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/v1/employees?skip=0&limit=50` | Список сотрудников с пагинацией |
| GET | `/api/v1/employees/{id}` | Профиль сотрудника |
| GET | `/api/v1/employees/{id}/subtree` | Поддерево сотрудника |
| GET | `/api/v1/employees/tree/roots` | Корневые узлы |

> Django и FastAPI — это два независимых сервера на разных портах, но **одна и та же БД**. Django пишет в дерево, FastAPI читает. Запускать из одной директории, иначе  разойдутся по разным файлам `db.sqlite3`.

---

## 2. Наполнение БД (seed.py, 50 000 сотрудников)

Скрипт генерирует случайную иерархию с реалистичными должностями и зарплатами по уровням.
Дефолты: `--amount 50000`, `--batch-size 10`, `--max-depth 5`, поэтому для 50 тысяч достаточно команды без аргументов.

Сначала обязательно примените миграции, затем из `online_employees_catalog/`:

```bash
poetry run python manage.py migrate
poetry run python seed.py --amount 50000 --batch-size 10 --max-depth 5
```

Параметры:

- `--amount` — сколько сотрудников сгенерировать
- `--batch-size` — размер пакета обработки (выбирается один начальник для пакета)
- `--max-depth` — максимальная глубина иерархии

> Генерация 50 000 записей небыстрая: каждый узел вставляется отдельно через `add_child()` (материализованный путь treebeard пересчитывается на каждой вставке). Для разработки используйте небольшое значение, например `--amount 1000`.

---

## 3. О проекте и технологиях

### Суть

Сотрудники образуют дерево: корневой узел (CEO) → руководители → рядовые специалисты. У каждого сотрудника есть имя, должность, дата приёма и зарплата. Проект умеет:

- показывать каталог сотрудников постранично, включая поддерево конкретного руководителя;
- отдавать те же данные в виде асинхронного JSON API;
- массово генерировать тестовые данные.

Для хранения дерева используется **материализованный путь** (materialized path): в каждом узле хранится `path` (например `00010002`), `depth` (глубина, корень = 1) и `numchild`. Поэтому выборка поддерева — это `WHERE path LIKE 'путь%'`, а порядок детей задаётся полем `node_order_by = ['role', 'name']`.

Ключевое ограничение: записи в таблицу `employee_catalog_employee` должны идти только через Django/treebeard (`add_root()` / `add_child()`), иначе поля `path`/`depth`/`numchild` станут некорректными и дерево сломается. FastAPI работает с этой же таблицей только на чтение.

### Стек

| Технология | Роль |
|------------|------|
| Django 4.1 | веб-каталог, админка, миграции, запись дерева |
| django-treebeard (MP_Node) | иерархия сотрудников (materialized path) |
| FastAPI | асинхронное REST API |
| SQLAlchemy 2.0 (async) | асинхронный доступ к БД в API |
| Pydantic v2 | схемы запросов/ответов и валидация |
| Uvicorn | ASGI-сервер для FastAPI |
| SQLite / PostgreSQL | БД: `aiosqlite` для API, `psycopg2` для Django, `asyncpg` для Postgres |
| python-decouple / python-dotenv | загрузка настроек из `.env` |
| names-generator | генерация имён в seed.py |
| Poetry | управление зависимостями и виртуальным окружением |

### Структура

```
online_employees_catalog/          # рабочий корень проекта (manage.py, seed.py)
├── manage.py
├── seed.py                        # генератор 50k сотрудников
├── online_employees_catalog/      # настройки Django проекта
│   └── settings.py
├── employee_catalog/              # Django-приложение: модель Employee, views, urls
└── fastapi_api/                   # FastAPI-приложение
    ├── main.py                    # точка входа, подключает роутеры
    ├── config.py                  # настройки и DATABASE_URL
    ├── database.py                # async engine и сессии
    ├── models.py                  # SQLAlchemy-модель таблицы treebeard
    ├── crud.py                    # запросы к БД
    ├── schemas.py                 # Pydantic-схемы
    └── routers/employees.py       # эндпоинты /api/v1/employees
tests/                             # тесты (pytest)
conftest.py
```

Итоговые префиксы API собираются из двух мест: `app.include_router(..., prefix="/api")` в `main.py` плюс `APIRouter(prefix="/v1/employees")` в роутере → `/api/v1/employees`.
