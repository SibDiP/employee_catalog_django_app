"""
Модуль конфигурации для FastAPI приложения к employee_catalog
Загружает настройки из .env
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# __file__ - отдаёт строку положения файла в системе
# Path() - превращает в объект pathlib.PosixPath. Фишки:
# * удобные для навигации методы
# 
BASE_DIR = Path(__file__).resolve().parent.parent

# символ / в pathlib.PosixPath перегружен. Подставляет / либо \ в зависимости от OS
env_path = BASE_DIR / '.env'

from pathlib import Path
from dotenv import load_dotenv



# Чтобы убедиться, что путь теперь правильный, включите режим отладки (verbose=True)
load_dotenv(dotenv_path=env_path, verbose=True)

print(f"Файл существует? {env_path.exists()}") # Должно вывести True