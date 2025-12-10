"""Fulfill DB with fake employees
Run from shell
"""
# TODO add a first employee creation logic
from decouple import config
import os
# Читаем из .env имя модуля настроек
settings_module = config('DJANGO_SETTINGS_MODULE', default='online_employees_catalog.settings')
# прокидываем в настоящие переменные окружения, что б джанго его увидал
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
# Теперь django.setup() увидит нужные настройки
import django
django.setup()
from django.db import transaction
from employee_catalog.models import Employee
import random
from names_generator import generate_name
from datetime import datetime, timedelta


# Константы можно менять по желанию
EMPLOYEE_AMOUNT = 50
EMPLOYEE_PER_CHIEF_AMOUNT = 5
HIERARCHY_LVL_MAX_DEEP = 5
EMPLOYEE_ROLES: dict[int, tuple[str]] = {
    # Сгенерированно ИИ
    # C-level executives
    0: ('CEO', 'President'),

    # Vice Presidents и Directors
    1: (
        'VP Sales', 'VP Engineering', 'VP Marketing', 'VP Operations',
        'Director of HR', 'Chief Financial Officer (CFO)',
        'Chief Technology Officer (CTO)', 'Chief Product Officer (CPO)',
    ),
    
    # Managers и Senior Leads
    2: (
        'Engineering Manager', 'Product Manager', 'Sales Manager',
        'Team Lead', 'Scrum Master', 'Tech Lead',
        'QA Lead', 'Design Lead',
    ),
    
    # Senior Individual Contributors
    3: (
        'Senior Developer', 'Senior QA Engineer', 'Senior Designer',
        'Security Engineer', 'DevOps Engineer',
        'Solutions Architect', 'Senior Product Designer',
    ),
    
    # Junior/Mid-level Individual Contributors
    4: (
        'Software Developer', 'Frontend Developer', 'Backend Developer',
        'QA Engineer', 'UI/UX Designer', 'Data Analyst',
        'Junior Developer', 'Quality Assurance',
    ),
}
SALARY_RANGES: dict[int, tuple[int, int]] = {
    0: (400_000, 600_000),  # CEO
    1: (150_000, 300_000),  # VP/CTO/CFO
    2: (80_000, 150_000),   # Manager/Team Lead
    3: (50_000, 100_000),   # Senior Developer
    4: (30_000, 70_000),    # Developer/QA
}

iteration_amount = EMPLOYEE_AMOUNT // EMPLOYEE_PER_CHIEF_AMOUNT
iteration_remainder_amount = EMPLOYEE_AMOUNT % EMPLOYEE_PER_CHIEF_AMOUNT
today = datetime.now()


def custom_chief_provider(max_hierarchy_lvl) -> object:
    """Возвращает случайного руководителя с глубиной меньше max_hierarchy_lvl."""
    employees = Employee.objects.filter(depth__lt=max_hierarchy_lvl)
    # Вместо полностью случайного выбора
    employees = Employee.objects.filter(
        depth__lt=max_hierarchy_lvl,
        numchild__lt=EMPLOYEE_PER_CHIEF_AMOUNT  # Не даём начальнику >  X подчинённых
    )
    if employees.exists():
        return random.choice(employees)
    else:
        root = Employee.add_root(name=generate_name(style='capital'),
                           employment_date = today - timedelta(days=random.randint(1, 365 * 5)),
                           role = {generator_employee_role(0)},
                           salary = generate_salary(0),
                           )
        return root

def generator_employee_role(depth_lvl: int) -> str:
    """Возвращает случайную должность из списка на основе depth."""
    role = EMPLOYEE_ROLES.get(depth_lvl, ('Employee',))
    return random.choice(role)

def generate_salary(depth: int) -> int:
    """Генерирует адекватную зарплату на основе уровня иерархии.

    Returns:
        int: Зарплата в виде целого числа.
    """
    min_sal, max_sal = SALARY_RANGES.get(depth, (30_000, 50_000))
    return random.randint(min_sal, max_sal)

def employee_create(employee_per_chief: int, max_hierarchy_lvl: int) -> None:
    """Генерирует лист сотрудников и добавляет chef-у за один вызов add_children."""
    if not employee_per_chief:
        return
    
    chief = custom_chief_provider(max_hierarchy_lvl)
    employee_hierarchy_lvl = chief.depth + 1
    now = datetime.now()

    employees_data = [
        {
            'name': generate_name(style='capital'),
            'employment_date': now - timedelta(days=random.randint(1, 365 * 5)),
            'role': f"{generator_employee_role(employee_hierarchy_lvl)}",
            'salary': generate_salary(employee_hierarchy_lvl),

        }
        for _ in range(employee_per_chief)
    ]
    with transaction.atomic(): # делает одним INSERT. 
        for employee in employees_data:
            chief.add_child(
                name=employee['name'],
                employment_date=employee['employment_date'],
                role=employee['role'],
                salary=employee['salary']
                )
    print(f'{employee_per_chief} подчинённых добавлено к {chief.name} уровень {chief.depth}')

for i in range(iteration_amount):
    employee_create(EMPLOYEE_PER_CHIEF_AMOUNT, HIERARCHY_LVL_MAX_DEEP)

if iteration_remainder_amount:
    employee_create(iteration_remainder_amount, HIERARCHY_LVL_MAX_DEEP)