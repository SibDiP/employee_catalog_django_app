"""
Модуль конфигурации для FastAPI приложения к employee_catalog
Загружает настройки из .env
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from functools import cached_property

from sqlalchemy.engine import URL

# __file__ - отдаёт строку положения файла в системе
# Path() - превращает в объект pathlib.PosixPath. Фишки:
# * удобные для навигации методы
# 
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# символ / в pathlib.PosixPath перегружен. Подставляет / либо \ в зависимости от OS
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    """
    Класс для хранения настроек fastapi приложения.
    Использует свойства для ленивой загрузки параметров БД.
    """
    # Регистратор наличия созданного экземпляра класса
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self):
        # Регистрируем объект, для реализации синглтон паттерна
        if hasattr(self, '_initialized'):
            return
        self._initialized = True

        # Определяем SQLite или PostgreSQL
        self.USE_SQLITE = os.getenv('USE_SQLITE', 'True').lower() == 'true'

        # Настройки FastAPI
        self.API_TITLE = 'Employee Catalog API'
        self.API_VERSION = '0.1'
        self.API_DESCRIPTION = """
        Асинхронное API для работы с иерархическим каталогом сотрудников.
        
        ## Особенности:
        * Поддержка иерархической структуры (MP_Node из django-treebeard)
        * Пагинация для работы с 50k+ записей
        * Автоматическая документация (Swagger UI)
        
        ## Эндпоинты:
        * `/api/employees` - список сотрудников с пагинацией
        * `/api/employees/{id}` - профиль сотрудника
        * `/api/employees/{id}/subtree` - поддерево сотрудника
        * `/api/employees/tree/roots` - корневые узлы
        """

        # Настройки пагинации
        self.DEFAULT_PAGE_SIZE = 50 # по умолчанию Х записей на страницу
        self.MAX_PAGE_SIZE = 200 # максимум для защиты от перегрузки

        # Настройки БД
        self.DB_ECHO = False # True - выводить SQL запросы в консоль

        # Прочие настройки
        self.PORT = 8001


    @cached_property
    def DATABASE_URL(self) -> str:
        
        if self.USE_SQLITE:
            # SQLite: файловая БД, ассинхронный драйвер aiosqlite
            db_path = BASE_DIR / 'db.sqlite3'
            return f"sqlite+aiosqlite:///{db_path}"
        
        else:
            # PostgreSQL: используем параметры из .env
            db_port = os.getenv('DB_PORT', '5432')
            # asyncpg - асинхронный драйвер для PostgreSQL
            url = URL.create(
                drivername="postgresql+asyncpg",
                username=os.getenv('DB_USER'),
                password=os.getenv('DB_PASS'),
                host=os.getenv('DB_HOST', '127.0.0.1'),
                port=int(db_port) if db_port else None, # Порт должен быть числом или None
                database=os.getenv('DB_NAME'),
            )                
            return url.render_as_string(hide_password=False)
        
    @cached_property
    def DB_TYPE(self) -> str:
        """
        Возвращает тип БД
        """
        return "sqlite" if self.USE_SQLITE else "postgresql"

# Создаём экземпляр настроек
settings = Settings()


