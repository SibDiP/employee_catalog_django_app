from django.shortcuts import render
from .models import Employee

def employee_tree(request):
    root_nodes = Employee.get_root_nodes()
    return render(request, 'employee_catalog/employee_catalog_tree.html', {'root_nodes': root_nodes})
