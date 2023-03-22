# Generated by Django 4.1.7 on 2023-03-22 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_catalog', '0007_alter_employee_chief'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='depth',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='employee',
            name='numchild',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='employee',
            name='path',
            field=models.CharField(default='', max_length=100),
        ),
    ]
