from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Employee


class EmployeeAdmin(TreeAdmin):
    form = movenodeform_factory(Employee)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = "Управление сотрудниками"
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(Employee, EmployeeAdmin)
