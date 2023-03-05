from django import forms
from django.contrib import admin
from .models import Employee

class EmployeeAdminForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide the 'my_field' field in the instance creation form
        self.fields['hierarchy_lvl_counter'].widget = forms.HiddenInput()


class EmployeeAdmin(admin.ModelAdmin):
    list_display = 'name', 'role', 'chief', 'salary', 'employment_date'
    form = EmployeeAdminForm


admin.site.register(Employee, EmployeeAdmin)

