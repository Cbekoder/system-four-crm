# Generated by Django 5.1.6 on 2025-03-25 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='currency_type',
            field=models.CharField(choices=[('USD', 'USD🇺🇸'), ('UZS', 'UZS🇺🇿'), ('RUB', 'RUB🇷🇺')], default='UZS', max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='section',
            field=models.CharField(blank=True, choices=[('logistic', 'Logistika'), ('fridge', 'Muzlatgich'), ('garden', "Bog'"), ('factory', 'Zavod')], max_length=30, null=True),
        ),
    ]
