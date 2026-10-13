from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from decimal import Decimal

class EmployeeBase(BaseModel):
    """Общие для всех сотрудников поля"""
    name: str = Field(..., 
                      min_length=1, 
                      max_length=255,
                      description="Полное имя сотрудника")
    # name: str = Field(...)
    # ... (Ellipsis) - явно говоришь Pydantic: "У этого поля нет 
    # значения по умолчанию. Клиент обязан передать 
    # его в JSON запросе". Если клиент его не 
    # пришлет, FastAPI вернет ошибку валидации.
 
    role: str = Field(..., min_length=1, max_length=255, description="Должность")
    employment_date: date = Field(..., description="Дата приема на работу")
    # ge=0 гарантирует, что зарплата не будет отрицательной
    salary: Decimal = Field(..., ge=0, max_digits=10, decimal_places=2, description="Зарплата")

class EmployeeResponse(EmployeeBase):
    """Схема для полного ответа API (один сотрудник)."""
    id: int = Field(..., description="Уникальный идентификатор")
    path: str = Field(..., description="Путь в иерархии (MP_Node)")
    depth: int = Field(..., description="Глубина в дереве (0=корень)")
    numchild: int = Field(..., description="Количество прямых подчиненных")
    
    # allow_inf_nan=False защищает от некорректных дробных данных из БД
    model_config = ConfigDict(from_attributes=True, allow_inf_nan=False)

class EmployeeListItem(EmployeeBase):
    """Схема для элемента списка сотрудников (облегченная)."""
    id: int
    depth: int  # Нужна фронтендерам для отступов дерева в плоском списке
    
    model_config = ConfigDict(from_attributes=True)

# === Схемы для пагинации ===

class PaginationParams(BaseModel):
    """Параметры пагинации для Query-параметров GET-запросов."""
    skip: int = Field(0, ge=0, description="Сколько записей пропустить")
    limit: int = Field(50, ge=1, le=200, description="Сколько записей вернуть")

class PaginatedEmployeeResponse(BaseModel):
    """Итоговый конверт ответа с пагинацией и мета-данными."""
    items: list[EmployeeListItem] = Field(..., description="Список сотрудников на странице")
    total: int = Field(..., description="Общее количество сотрудников в БД")
    skip: int = Field(..., description="Сколько пропущено")
    limit: int = Field(..., description="Лимит на страницу")
    has_more: bool = Field(..., description="Есть ли еще записи на следующих страницах")

# === Схемы для деревьев ===

class TreeNode(BaseModel):
    """Узел рекурсивного дерева для фронтенда."""
    id: int
    name: str
    role: str
    depth: int
    # Использование 'TreeNode' (строкой) позволяет сослаться на самого себя
    children: list['TreeNode'] = Field(default_factory=list, description="Список подчиненных узлов")
    
    model_config = ConfigDict(from_attributes=True)

# Пересборка модели обязательна для Pydantic v2, чтобы разрешить циклическую ссылку
TreeNode.model_rebuild()