"""Fulfill DB with fake employees
Run from shell
"""
# TODO add a first employee creation logic
import django
django.setup()
from employee_catalog.models import Employee
import random
from names_generator import generate_name
from datetime import datetime, timedelta

# This three constants can be changed as needed
SEED_EMPLOYEE_AMOUNT = 50
SEED_EMPLOYEE_PER_CHIEF_AMOUNT = 5
SEED_HIERARCHY_LVL_MAX_DEEP = 5

seed_iteration_amount = SEED_EMPLOYEE_AMOUNT // SEED_EMPLOYEE_PER_CHIEF_AMOUNT
seed_iteration_remainder_amount = SEED_EMPLOYEE_AMOUNT % SEED_EMPLOYEE_PER_CHIEF_AMOUNT


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


for i in range(seed_iteration_amount):
    employee_create(SEED_EMPLOYEE_PER_CHIEF_AMOUNT, SEED_HIERARCHY_LVL_MAX_DEEP)

employee_create(seed_iteration_remainder_amount, SEED_HIERARCHY_LVL_MAX_DEEP)
