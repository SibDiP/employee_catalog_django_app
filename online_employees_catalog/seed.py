"""Fulfill DB with fake employees
Run from shell
"""

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
import argparse

from employee_catalog.models import Employee
import random
from names_generator import generate_name
from datetime import datetime, timedelta


# Константы можно менять по желанию
EMPLOYEE_AMOUNT = 50_000
EMPLOYEE_PER_BATCH  = 5
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


today = datetime.now()

######################################################################
# Tools

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


######################################################################
# Main func

def create_CEO() -> Employee:
    """Создаёт корневую ноду в Employee"""
    ceo = Employee.objects.filter(depth=1).first()
    if ceo is None:
        ceo = Employee.add_root(
                            name=generate_name(style='capital'),
                            employment_date = today - timedelta(days=random.randint(1, 365 * 5)),
                            role = generator_employee_role(0),
                            salary = generate_salary(0),
                            )
        print("CEO создан")
    return ceo

def get_random_chief_list(max_depth: int, amount: int) -> list[Employee]:
    """Получить лист случайных Employee в БД с depth HIERARCHY_LVL_MAX_DEEP - 1 (т.к. нижний
    уровень не может быть руководителелем).

    Args:
        max_depth (int): Максимальная глубина запроса.
        amount(int): количество записей.

    Raises:
        TypeError: необходимо задать max_depth
        TypeError: необходимо задать amount

    Returns:
        lsit[Employee]: Список Employeeв бд с depth == max_depth-1
        
    """

    if max_depth == None:
        raise TypeError("Необходим max_depth") 
    if amount == None:
        raise TypeError("Необходим amount")
    
    chifs_depth = max_depth - 1
    all_chief_list = Employee.objects.filter(depth__lte=chifs_depth)
    chosen_chiefs = random.choices(all_chief_list, k=amount,)

    return chosen_chiefs
        
def create_employees_data(
        chief_list: list[Employee], max_depth: int
        ) -> list[dict]:
    """Генерирует данные сотрудника.

    Args:
        max_depth (int): Максимальная глубина в иерархии.

    Returns:
        dict: Словарь с данными Employee для вставки в БД.
    """

    now = datetime.now()
    chief = random.choice(chief_list)
    employee_hierarchy_lvl = chief.depth + 1

    employees_data = [
        {
            'chief': chief,
            'name': generate_name(style='capital'),
            'employment_date': now - timedelta(days=random.randint(1, 365 * 5)),
            'role': f"{generator_employee_role(employee_hierarchy_lvl)}",
            'salary': generate_salary(employee_hierarchy_lvl),
        }
        for _ in (chief_list)
    ]
    return employees_data

def insert_employees_data(employees_data: list[dict]):
    """Вставляет Employee в БД.add()
     
    Используется один INSERT с помощью transaction.atomic().

    transaction.atomic() используется в основном для ускорения генерации на HDD.

    Args:
        employees_data (list[dict]): лист со словарями. Один словарь - один Employee.
    """
    with transaction.atomic(): # делает одним INSERT. 
        for employee in employees_data:
            employee['chief'].add_child(
                name=employee['name'],
                employment_date=employee['employment_date'],
                role=employee['role'],
                salary=employee['salary']
                )

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--amount", type=int, default=EMPLOYEE_AMOUNT)
    parser.add_argument("--batch-size", type=int, default=EMPLOYEE_PER_BATCH)
    parser.add_argument("--max-depth", type=int, default=HIERARCHY_LVL_MAX_DEEP)
    # TODO - seed для возможности проверки работы
    #parser.add_argument("--seed", type=int, default=None)
    # TOD - повторный запуск / удаление записей


    args = parser.parse_args()

    iteration_amount = args.amount // args.batch_size
    iteration_remainder_amount = args.amount % args.batch_size

    current_iteration = 1
    total_iteration = iteration_amount
    if iteration_remainder_amount > 0:
        total_iteration += 1
    
    print(f"Генеририруем {args.amount} записей сотрудников")
    create_CEO()

    for batch in range(iteration_amount):
        chief_list = get_random_chief_list(args.max_depth, args.batch_size)
        employees_data = create_employees_data(chief_list, args.max_depth)
        insert_employees_data(employees_data)
        print(f"Добавлено {args.batch_size} сотрудников! | {current_iteration}/{total_iteration}")
        current_iteration += 1


    if iteration_remainder_amount > 0:
        chief_list = get_random_chief_list(args.max_depth, iteration_remainder_amount)
        employees_data = create_employees_data(chief_list, args.max_depth)
        insert_employees_data(employees_data)
        print(f"Добавлено {iteration_remainder_amount} сотрудников! | {current_iteration}/{total_iteration}")
