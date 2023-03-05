from datetime import datetime

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
        # need to be refreshed to update post_save logic
        self.chief_employee.refresh_from_db()

        self.employee_lvl_2_1 = Employee.objects.create(
            name='Джеки Чан',
            role='Поставновщик трюков',
            salary=200000,
            employment_date='2022-02-01',
            chief=self.chief_employee
        )
        self.employee_lvl_2_1.refresh_from_db()

        self.employee_lvl_2_2 = Employee.objects.create(
            name='Майкл Бей',
            role='Пиротехник',
            salary=200000,
            employment_date='2022-03-01',
            chief=self.chief_employee
        )
        self.employee_lvl_2_2.refresh_from_db()

    def test_employee_creation(self):
        self.assertEqual(self.chief_employee.name, 'Джо Денжер')
        self.assertEqual(self.chief_employee.role, 'Глава отдела тестирования')
        self.assertEqual(self.chief_employee.salary, 300000)
        self.assertEqual(self.chief_employee.employment_date, datetime.strptime('2023-01-01', '%Y-%m-%d').date())

    def test_employee_post_save_chief_and_hierarchy_update(self):
        self.assertEqual(self.chief_employee.chief, self.chief_employee)
        self.assertEqual(self.chief_employee.hierarchy_lvl_counter, 1)

    def test_employee_post_save_chief_and_hierarchy_update_lvl_2(self):
        self.assertEqual(self.employee_lvl_2_1.chief, self.chief_employee)
        self.assertEqual(self.employee_lvl_2_1.hierarchy_lvl_counter, 2)
        self.assertEqual(self.employee_lvl_2_2.chief, self.chief_employee)
        self.assertEqual(self.employee_lvl_2_2.hierarchy_lvl_counter, 2)







    # def test_two_second_lvl_employee(self):
    #     employee1 = Employee.objects.create(
    #         name='Джеки Чан',
    #         role='Поставновщик трюков',
    #         salary=200000,
    #         employment_date='2022-02-01',
    #         chief=self.employee
    #     )
    #     employee2 = Employee.objects.create(
    #         name='Майкл Бей',
    #         role='Пиротехник',
    #         salary=200000,
    #         employment_date='2022-03-01',
    #         chief=self.employee
    #     )
    #     self.assertEqual(employee1.chief, self.employee)
    #     self.assertEqual(employee2.chief, self.employee)
    #     self.assertEqual(employee2.hierarchy_lvl_counter, 1)
    #     self.assertEqual(employee2.hierarchy_lvl_counter, 1)

