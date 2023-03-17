from django.db.models import QuerySet
from django.shortcuts import render, get_object_or_404
from .models import Employee


# by hierarchy lvl 1
def employee_tree(request) -> QuerySet:
    employees = Employee.objects.filter(hierarchy_lvl_counter=1)
    context = {'lvl_1_employees': employees}
    print(type(employees))
    return render(request, 'employee_catalog/employee_catalog_tree.html', context)


# by objects_list ->
def specific_employee_tree(request, pk):
    pass
    # employee = get_object_or_404(Employee, pk=pk)
    # employees = employee.employee_set.all
    # context = {'employees': employees}
    #
    # return render(request, 'employee_catalog/employee_catalog_tree.html', context)
