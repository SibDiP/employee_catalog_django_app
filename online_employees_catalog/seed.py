"""Fulfill DB with fake employees
Run from shell
"""

import django
django.setup()
from django_seed import Seed
from employees_catalog_app.models import Employee
import random
from names_generator import generate_name

# This three constants can be changed as needed
SEED_EMPLOYEE_AMOUNT = 999
SEED_EMPLOYEE_PER_CHIEF_AMOUNT = 50
SEED_HIERARCHY_LVL_MAX_DEEP = 5

seed_iteration_amount = SEED_EMPLOYEE_AMOUNT // SEED_EMPLOYEE_PER_CHIEF_AMOUNT
seed_iteration_remainder_amount = SEED_EMPLOYEE_AMOUNT % SEED_EMPLOYEE_PER_CHIEF_AMOUNT


def custom_chief_provider(max_hierarchy_lvl) -> object:
    """
    :return: random employee with hierarchy_lvl less than 5
    """
    employees = Employee.objects.filter(hierarchy_lvl_counter__lt=max_hierarchy_lvl)

    if employees.exists():
        return random.choice(employees)
    else:
        return None


def employee_create(employee_per_chief: int, max_hierarchy_lvl: int) -> None:
    seeder = Seed.seeder()
    chief = custom_chief_provider(max_hierarchy_lvl)
    employee_hierarchy_lvl = chief.hierarchy_lvl_counter + 1

    for _ in range(employee_per_chief):
        seeder.add_entity(Employee, 1, {
            'name': generate_name(style='capital'),
            'role': f"Employee lvl {employee_hierarchy_lvl}",
            'salary': round(random.random()*1000),
            'chief': chief
        })
    seeder.execute()
    print(f'{employee_per_chief} employees added')


for i in range(seed_iteration_amount):
    employee_create(SEED_EMPLOYEE_PER_CHIEF_AMOUNT, SEED_HIERARCHY_LVL_MAX_DEEP)

employee_create(seed_iteration_remainder_amount, SEED_HIERARCHY_LVL_MAX_DEEP)
