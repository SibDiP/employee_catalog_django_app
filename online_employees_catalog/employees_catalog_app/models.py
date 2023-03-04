from django.db import models
from django.db.models.signals import post_save


class Employee(models.Model):
    """Model for employees information"""
    name = models.CharField('Имя', max_length=255)
    role = models.CharField('Должность', max_length=255)
    # TODO add positive salary validator
    salary = models.FloatField('Заработная плата')
    employment_date = models.DateField('Дата приёма на работу')
    chief = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


def employee_post_save_chief_check(sender, instance, *args, **kwargs):
    """Make an employee chief for himself if None is chosen when create"""
    if instance.chief is None:
        self_chief = instance
        self_chief.chief = instance
        self_chief.save()


post_save.connect(employee_post_save_chief_check, sender=Employee)
