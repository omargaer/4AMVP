# Generated by Django 5.1.4 on 2025-01-09 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0021_remove_applicationstatushistory_unique_application_status_history_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationsla',
            name='acceptanceDate',
            field=models.DateField(null=True, verbose_name='Дата принятия'),
        ),
        migrations.AlterField(
            model_name='applicationsla',
            name='completionDate',
            field=models.DateField(null=True, verbose_name='Дата закрытия'),
        ),
        migrations.AlterField(
            model_name='applicationsla',
            name='creationDate',
            field=models.DateField(null=True, verbose_name='Дата создания'),
        ),
    ]
