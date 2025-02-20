# Generated by Django 5.1.4 on 2025-01-06 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0019_alter_applicationactions_timestamp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='account',
            name='last_name',
        ),
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
    ]
