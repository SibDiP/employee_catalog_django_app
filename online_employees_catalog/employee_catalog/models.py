from django.db import models
from django.db.models.signals import post_save, pre_save
from django.core.exceptions import ValidationError


class Employee(models.Model):
    """Model for employees information"""
    name = models.CharField('Имя', max_length=255)
    role = models.CharField('Должность', max_length=255)
    # TODO add positive salary validator
    salary = models.FloatField('Заработная плата')
    employment_date = models.DateField('Дата приёма на работу')
    chief = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Начальник', null=True, blank=True,
                              limit_choices_to={'hierarchy_lvl_counter__lt': 5}
                              )

    hierarchy_lvl_counter = models.PositiveSmallIntegerField('Уровень иерархии', null=True, blank=True, )

    def __str__(self):
        return f'{self.name}, lvl-{self.hierarchy_lvl_counter}'


def employee_post_save_chief_and_hierarchy_update(sender, instance, *args, **kwargs):
    """Make an employee chief for himself if None is chosen when create and give a hierarchy lvl"""
    if instance.chief is None:
        Employee.objects.filter(pk=instance.pk).update(chief=instance, hierarchy_lvl_counter=1)
    else:
        instance_hierarchy_lvl_counter = instance.chief.hierarchy_lvl_counter + 1
        Employee.objects.filter(pk=instance.pk).update(hierarchy_lvl_counter=instance_hierarchy_lvl_counter)


post_save.connect(employee_post_save_chief_and_hierarchy_update, sender=Employee)
