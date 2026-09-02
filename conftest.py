import pytest
from datetime import date

from employee_catalog.models import Employee


@pytest.fixture
def ceo(db):
    return Employee.objects.add_root(
        create_kwargs={
            "name": "CEO",
            "role": "President",
            "salary": 500000,
            "employment_date": date(2023, 1, 1),
        }
    )


@pytest.fixture
def manager(ceo):
    return Employee.objects.add_child(
        ceo,
        create_kwargs={
            "name": "Manager",
            "role": "Engineering Manager",
            "salary": 150000,
            "employment_date": date(2023, 2, 1),
        }
    )


@pytest.fixture
def developer(manager):
    return Employee.objects.add_child(
        manager,
        create_kwargs={
            "name": "Developer",
            "role": "Backend Developer",
            "salary": 90000,
            "employment_date": date(2023, 3, 1),
        }
    )
