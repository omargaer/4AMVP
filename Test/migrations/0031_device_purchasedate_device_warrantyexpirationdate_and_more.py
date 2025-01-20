# Generated by Django 5.1.4 on 2025-01-20 02:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0030_alter_individualentity_inipa_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='purchaseDate',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Дата покупки'),
        ),
        migrations.AddField(
            model_name='device',
            name='warrantyExpirationDate',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Дата окончания гарантии'),
        ),
        migrations.AlterField(
            model_name='branchoffice',
            name='type',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, to='Test.branchofficetype', verbose_name='Тип филиала'),
        ),
    ]
