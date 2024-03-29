# Generated by Django 4.1.7 on 2023-03-02 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee_catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='self_chief',
            field=models.BooleanField(default=False, verbose_name='Сам себе начальник'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='chief',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='employee_catalog.employee'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='role',
            field=models.CharField(max_length=255, verbose_name='Должность'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='salary',
            field=models.FloatField(verbose_name='Заработная плата'),
        ),
    ]
