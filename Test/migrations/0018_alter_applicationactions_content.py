# Generated by Django 5.1.4 on 2024-12-29 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0017_alter_device_factorynumber_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationactions',
            name='content',
            field=models.CharField(default='', max_length=300, verbose_name='Описание действия'),
        ),
    ]