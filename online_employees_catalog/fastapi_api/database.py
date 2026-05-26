"""
Модуль работы с БД
Создаёт асинхронный движок, фабрику сессий и dependency для эндпоинтов
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from .config import settings

# Создаём асинхронный engine
# - пул соединений с БД для PostgreSQL и одно для SQLite
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,  # Логирование SQL в консоль

    # Дополнительные параметры для SQLite
    # По умолчанию SQLite разрешает доступ к файлу базы данных только из того потока 
    # (Thread), в котором она была создана. Поскольку FastAPI работает асинхронно и 
    # обрабатывает запросы в многопоточном цикле событий (Event Loop), без этого флага 
    # приложение упадет с ошибкой при попытке параллельного обращения двух разных 
    # пользователей. Этот флаг отключает проверку потоков, перекладывая контроль 
    # конкурентности на драйвер aiosqlite.
    connect_args=({"check_same_thread": False} 
                  if settings.USE_SQLITE 
                  else {}
                  )
)

# Создаём фабрику сессий
# SessionLocal - создаёт новые сессии для каждого запроса
AsyncSessionLocal = async_sessionmaker(
    engine,
    # Без сброса объектов после commit().
    # ОБЯЗАТЕЛЬНО для async работы с ORM. В противном случае, при обращении к объекту
    # будет совершаться новый запрос в БД для обновления данных
    expire_on_commit=False,
)

# MetaData для работы с существующей схемой БД
# позволяет "отразить" уже существующие таблицы. На момент создания - пуст.
# Наполнится после описания модели SQLAlchemy.
metadata = MetaData()

class Base(DeclarativeBase):
    """
    Базовый класс для всех ORM-моделей в стиле SQLAlchemy 2.0.
    Явно связан с кастомным объектом metadata для поддержки отражения таблиц Django.
    """
    metadata = metadata

# В аннотациях типов для генераторов всегда указываются два (или три) фиксированных 
# параметра через запятую: AsyncGenerator[Тип_Выдачи (Yield Type), Тип_Приёма(Send Type)]
# AsyncGenerator - указывает на то, что функция есть ассик_генератор с yield вместо return
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """DEPENDENCY: Функция для получения сессии БД в эндпоинтах.

    Использование:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            ...
    
    Важно: 
        - async with гарантирует автоматическое закрытие сессии
        - yield передает сессию в эндпоинт
        - finally выполняется после завершения запроса
    """
    # Контекстный менеджер async with гарантирует автоматический вызов session.close()
    async with AsyncSessionLocal() as session:
        yield session

"""
## Объяснение функции async def get_db() что б не забывал:

async def get_db() -> AsyncGenerator[AsyncSession, None]:

async def — делает функцию асинхронной корутиной. Это нужно, 
    так как создание и закрытие сессий в асинхронной архитектуре задействует 
    асинхронные механизмы.    
async with AsyncSessionLocal() as session:
AsyncSessionLocal() — вызывает фабрику (которую мы настроили ранее) и создает 
    новый, чистый объект сессии (соединения с БД).

async with ... as session — это 
    асинхронный контекстный менеджер. У него есть два скрытых метода: __aenter__ 
    (срабатывает в начале) и __aexit__ (срабатывает в самом конце). Как только код 
    выйдет из блока async with, этот менеджер автоматически вызовет 
    await session.close(). Никакие ошибки или исключения не смогут это 
    предотвратить.
as session — сохраняет созданную сессию в переменную с именем session.
yield session
    yield — это «пауза» и «передача». В этот момент функция get_db 
    замораживается. Она отдает переменную session наружу — в твой эндпоинт 
    FastAPI (туда, где написано db: AsyncSession = Depends(get_db)).Эндпоинт 
    делает свою работу: запрашивает пользователей, сохраняет данные, делает 
    коммит.Как только эндпоинт закончил работу и FastAPI сформировал HTTP-ответ 
    для клиента, FastAPI возвращается сюда и «снимает» функцию get_db с паузы.
    Код шагает дальше, упирается в конец блока async with, и сессия благополучно 
    закрывается.
    """