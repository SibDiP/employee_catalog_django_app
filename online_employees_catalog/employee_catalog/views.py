from django.shortcuts import render
from .models import Employee


def employee_tree(request):
    employees = Employee.objects.all()
    context = {'employees': employees}
    return render(request, 'employee_catalog/employee_catalog_tree.html', context)
