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

# This three constants can be changed as needed
SEED_EMPLOYEE_AMOUNT = 50
SEED_EMPLOYEE_PER_CHIEF_AMOUNT = 5
SEED_HIERARCHY_LVL_MAX_DEEP = 5
EMPLOYEE_ROLES: dict[int, tuple[str]] = {
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
        'Data Analyst', 'Security Engineer', 'DevOps Engineer',
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

seed_iteration_remainder_amount = SEED_EMPLOYEE_AMOUNT % SEED_EMPLOYEE_PER_CHIEF_AMOUNT
today = datetime.now()


def custom_chief_provider(max_hierarchy_lvl) -> object:
    """
    :return: random employee with hierarchy_lvl less than 5
    """
    employees = Employee.objects.filter(depth__lt=max_hierarchy_lvl)

    if employees.exists():
        return random.choice(employees)
    else:
        root = Employee.add_root(name=generate_name(style='capital'),
                           employment_date=datetime.now() - timedelta(days=random.randint(1, 365 * 5)),
                           role=f"Chief",
                           salary=round(random.random() * 10000))
        return root


def employee_create(employee_per_chief: int, max_hierarchy_lvl: int) -> None:
    chief = custom_chief_provider(max_hierarchy_lvl)
    employee_hierarchy_lvl = chief.depth + 1

    for _ in range(employee_per_chief):
        employee = Employee.add_child(chief, name=generate_name(style='capital'),
                                      employment_date=datetime.now() - timedelta(days=random.randint(1, 365 * 5)),
                                      role=f"Employee lvl {employee_hierarchy_lvl}",
                                      salary=round(random.random() * 1000))

    print(f'{employee_per_chief} employees added to {chief}')
def generator_employee_role(depth_lvl: int) -> str:
    """Возвращает случайную должность из списка на основе depth"""
    role = EMPLOYEE_ROLES.get(depth_lvl, ('Employee',))
    return random.choice(role)

def generate_salary(depth: int) -> int:
    """
    Генерирует адекватную зарплату на основе уровня иерархии.

    Returns:
        Зарплата в виде целого числа
    """
    min_sal, max_sal = SALARY_RANGES.get(depth, (30_000, 50_000))
    return random.randint(min_sal, max_sal)

employee_create(seed_iteration_remainder_amount, SEED_HIERARCHY_LVL_MAX_DEEP)
