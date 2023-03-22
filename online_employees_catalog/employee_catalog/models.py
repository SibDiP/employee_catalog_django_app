from django.db import models
from treebeard.mp_tree import MP_Node

class Employee(MP_Node):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    employment_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.name} | {self.role}'
