import random
import django
django.setup()
from django_seed import Seed
from employees_catalog_app.models import Employee


def custom_chief_provider():
    # Get all employees with a hierarchy_lvl_counter less than 5
    employees = Employee.objects.filter(hierarchy_lvl_counter__lt=5)
    # Select a random employee from the list
    if employees.exists():
        return random.choice(employees)
    else:
        return None


seeder = Seed.seeder()

# Register the custom provider for the 'chief' field
for i in range(1,49900):
    seeder.add_entity(Employee, 1, {
        'chief': custom_chief_provider()
    })
    seeder.execute()

