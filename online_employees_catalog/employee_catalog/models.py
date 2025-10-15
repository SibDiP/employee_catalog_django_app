from django.db import models
from treebeard.mp_tree import MP_Node
from django.core.validators import MinValueValidator

class Employee(MP_Node):
    """
    Модель сотрудника с иерархической структурой
    
    MP_Node (Materialized Path Node) автоматически добавляет поля:
    - path: CharField(max_length=255) - полный путь от корня, вид:'00010002'
    - depth: PositiveIntegerField - глубина в дереве (0 = корень)
    - numchild: PositiveIntegerField - количество прямых потомков

    Полезные методы для работы с деревом:
    add_root(): создать корень.
    add_child(): добавить прямого потомка.
    get_ancestors() / get_parent(): навигация вверх по дереву.
    get_descendants() / get_children(): навигация вниз.
    get_siblings(): получить «братьев» на том же уровне.
    move(): переместить узел внутри дерева.

    """

    name = models.CharField('Имя', max_length=255)
    role = models.CharField('Должность', max_length=255)
    employment_date = models.DateField('Дата приёма на работу')
    salary = models.DecimalField(
        'Заработная плата',
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(
                0.00, message='Зарплата не может быть отрицательной')
        ])
    
    # Атрибут MP_Node. Порядок детей с начала по role, затем по name
    node_order_by = ['role', 'name']

    class Meta:
        """
        Класс с мета информацией Django (в БД не идёт)
        """
        # Отображение в админке
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.role} | {self.name} | уровень иерархии {self.depth}'
    
    @property
    def hierarchy_lvl(self):
        """
        Человекопонятное представление глубины иерархии.
        """
        return self.depth + 1
        
