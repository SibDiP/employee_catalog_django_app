# Generated by Django 4.1.7 on 2023-03-22 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_catalog', '0008_employee_depth_employee_numchild_employee_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='path',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
