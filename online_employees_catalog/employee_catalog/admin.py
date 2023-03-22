from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Employee


class EmployeeAdmin(TreeAdmin):
    form = movenodeform_factory(Employee)


admin.site.register(Employee, EmployeeAdmin)
