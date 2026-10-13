"""
Модели SQLAlchemy для работы с БД.
Описывают структуру таблиц, созданных Django с treebeard.
"""

from datetime import date
from decimal import Decimal
from sqlalchemy import (
    # String и Numeric — это типы данных на уровне SQL. Они нужны, чтобы объяснить базе 
    # данных точные параметры колонок (например, String(255) ограничит длину в таблице,
    # а Numeric(10, 2) укажет СУБД хранить числа с фиксированной запятой)
    String, Numeric, 
    # select — функция для построения SQL-запросов (замена старому стилю db.query()). 
    # Она понадобится чуть ниже, внутри реализации hybrid_property.expression.
    select
    )

from sqlalchemy.orm import (
    # Mapped[...] — это специальный generic-класс (обертка). Он сообщает анализатору типов 
    # (IDE), что данное поле является колонкой таблицы и при обращении вернет указанный 
    # внутри тип.
    # Пример: name: Mapped[str] — для IDE это обычная строка str, для SQLAlchemy — сигнал 
    # создать текстовую колонку.
    Mapped, 
    # mapped_column — функция, которая настраивает свойства этой колонки в самой базе 
    # данных (флаги primary_key, nullable, index, unique)
    mapped_column
    )
    # hybrid_property — декоратор, создающий «гибридное» свойство. Оно уникально тем, 
    # что работает в двух мирах одновременно: и в коде Python (как обычный @property), 
    # и на уровне генерации SQL-запросов (позволяет базе данных фильтровать и 
    # сортировать данные по вычисляемому полю).
from sqlalchemy.ext.hybrid import hybrid_property
from .database import Base


class Employee(Base):
    """ 
    Модель сотрудника, совместимая с django-treebeard MP_Node.
    Таблица в БД: employee_catalog_employee
    """
    __tablename__ = "employee_catalog_employee"

    # === Поля, созданные Django (стиль SQKAlchemy 2.0)
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(255), nullable=False)
    employment_date: Mapped[date] = mapped_column(nullable=False)

    # для чисел с плавающей запятой используем Numeric(кол-во цифр, цифр после запятой)
    salary: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    # === Поля MP_Node от treebeard
    # path - материализованный путь (например: '000100020003')
    # depth - глубина в дереве (0=корень, 1=первый уровень, и т.д.)
    # numchild - количество прямых потомков
    path: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    depth: Mapped[int] = mapped_column(nullable=False, default=0)
    numchild: Mapped[int] = mapped_column(nullable=False, default=0)

    @hybrid_property
    def full_name(self) -> str:
        """Полное имя (вычисляемое поле, не в БД)"""
        return f"{self.name} ({self.role})"
    
    @full_name.expression
    def full_name(cls):
        """ 
        Полное имя для вычислений в БД (внутри SQL-запросов)
        Правильно склеивает строки на уровне SQL.
        """
        return cls.name + " (" + cls.role + ")"
    
    def __repr__(self):
        return f"<Employee(id={self.id}, name={self.name}, role={self.role}, depth={self.depth})>"
    