# Generated by Django 4.1.7 on 2023-03-02 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees_catalog_app', '0002_employee_self_chief_alter_employee_chief_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='self_chief',
        ),
    ]