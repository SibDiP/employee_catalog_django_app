from django.contrib import admin
from .models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    list_display = 'name', 'role', 'chief', 'salary', 'employment_date'

admin.site.register(Employee, EmployeeAdmin)

