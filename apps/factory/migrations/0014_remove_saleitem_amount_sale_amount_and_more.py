# Generated by Django 5.1.6 on 2025-03-08 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factory', '0013_alter_sale_options_remove_sale_amount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saleitem',
            name='amount',
        ),
        migrations.AddField(
            model_name='sale',
            name='amount',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='sale',
            name='currency_type',
            field=models.CharField(choices=[('USD', 'USD🇺🇸'), ('UZS', 'UZS🇺🇿'), ('RUB', 'RUB🇷🇺')], default='UZS', max_length=20),
        ),
    ]
