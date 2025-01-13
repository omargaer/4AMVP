# Generated by Django 5.1.4 on 2025-01-10 14:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0024_remove_account_branchoffices_branchofficeemployees_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branchofficeemployees',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Test.individualentity', verbose_name='Физическое лицо'),
        ),
        migrations.AlterField(
            model_name='branchofficeschedule',
            name='closing_time',
            field=models.TimeField(blank=True, null=True, verbose_name='Время закрытия'),
        ),
        migrations.AlterField(
            model_name='branchofficeschedule',
            name='opening_time',
            field=models.TimeField(blank=True, null=True, verbose_name='Время открытия'),
        ),
    ]