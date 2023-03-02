from django.db import models

class Employee(models.Model):
    """Model for employees information"""
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    # TODO add positive salary validator
    salary = models.FloatField()
    chief = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    employment_date = models.DateField('Дата приёма на работу')



