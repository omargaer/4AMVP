# Generated by Django 5.1.4 on 2024-12-14 16:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0010_applicationpriority_applicationstatus_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='role',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, to='Test.accountrole', verbose_name='Роль'),
        ),
        migrations.AlterField(
            model_name='account',
            name='status',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, to='Test.accountstatus', verbose_name='Статус'),
        ),
    ]
