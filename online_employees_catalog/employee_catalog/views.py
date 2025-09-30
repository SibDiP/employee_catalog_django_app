from django.shortcuts import render, get_object_or_404
from .models import Employee


def specific_employee_tree(request, **kwargs):
    node_pk = kwargs.get('pk')
    root_node = get_object_or_404(Employee, pk=node_pk)
    return render(request, 'employee_catalog/employee_catalog_tree.html', {'root_nodes': (root_node,)})


def employee_tree(request):
    root_nodes = Employee.get_root_nodes()
    return render(request, 'employee_catalog/employee_catalog_tree.html', {'root_nodes': root_nodes})
