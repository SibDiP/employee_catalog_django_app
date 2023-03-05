from django.test import TestCase
from django.utils import timezone
from .models import Employee


class EmployeeCreateTestCase(TestCase):
    def setUp(self):
        self.chief_employee = Employee.objects.create(
            name='Джо Денжер',
            role='Глава отдела тестирования',
            salary=300000,
            employment_date='2023-01-01'
        )

    def test_employee_creation(self):
        self.assertEqual(self.chief_employee.name, 'Джо Денжер')
        self.assertEqual(self.chief_employee.role, 'Глава отдела тестирования')
        self.assertEqual(self.chief_employee.salary, 300000)
        self.assertEqual(self.chief_employee.employment_date, '2023-01-01')
