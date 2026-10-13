from employee_catalog.models import Employee


def test_tree_depth(ceo, manager, developer):
    assert ceo.depth == 1
    assert manager.depth == 2
    assert developer.depth == 3


def test_parent_and_children(ceo, manager):
    assert Employee.objects.get_parent(manager).pk == ceo.pk
    assert list(Employee.objects.get_children(ceo)) == [manager]


def test_descendants(ceo, manager, developer):
    assert Employee.objects.get_descendant_count(ceo) == 2
