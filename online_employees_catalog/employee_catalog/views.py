from django.shortcuts import render, get_object_or_404
from .models import Employee


def employee_tree(request):
    employees = Employee.get_root_nodes()
    return render(request, 'employee_catalog/employee_catalog_tree.html', {'employees': employees})

def specific_employee_tree(request, **kwargs):
    node_pk = kwargs.get('pk')
    employees = get_object_or_404(Employee, pk=node_pk)
    return render(request, 'employee_catalog/employee_catalog_tree.html', {'employees': [(employees)]})

# Предрассчёт дерева сотрудников (необходиммо т.к. БД на 50к+ записей)
def build_tree(nodes:list[Employee]):
    """
    Рассчёт дерева сторудников.

    nodes: объекты класса Employee

    return:
    list[dict] - лист со ссылками и деревья

    """
    # ссылки на корневые ноды в lookup
    tree = []
    # словарь с вложеннными словарями нод и их children
    lookup = {}

    # Создаём поля для всех сотрудников
    for node in nodes:
        lookup[node.pk] = {'node': node, 'children': []}
    # Заполняем поля дочерних нод
    for node in nodes:
        parent = node.get_parent()
        if parent:
            lookup[parent.pk]['children'].append(lookup[node.pk])
        else:
            tree.append(lookup[node.pk])
    return tree

def company_tree(request):
    """
    Передача дерева всех сотрудников в темплейт
    """
    all_nodes = Employee.get_tree()
    tree = build_tree(all_nodes)
    return render(request, 'employee_catalog/company_tree.html', 
    {
        'tree': tree,
        'page_title': 'Структура компании',
    })    



# Ниже учебно-тренеровочные вьюшки

def simple(request):
    employee = Employee.objects.get(pk=1)
    return render(request, 'employee_catalog/study/simple.html', 
    { 'employee': employee})

def show_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    context = {
        'employee': employee,
        'page_title': 'Профиль',
        'current_year': 2025,
    }

    return render(request, 'employee_catalog/study/show_employee.html', context)

def show_employee_full(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee_team = employee.get_descendants()
    employee_head = employee.get_parent() 

    context = {
        'employee': employee,
        'page_title': 'Профиль сотрудника',
        'head': employee_head,
        'team': employee_team,
        'current_year': 2025,
    }

    return render(request, 'employee_catalog/study/employee_full.html', context)



