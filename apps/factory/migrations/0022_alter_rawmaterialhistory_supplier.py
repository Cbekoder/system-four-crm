# Generated by Django 5.1.5 on 2025-03-23 17:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factory', '0021_remove_rawmaterial_currency_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawmaterialhistory',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='factory.supplier'),
        ),
    ]
