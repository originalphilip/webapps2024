# Generated by Django 5.0.3 on 2024-04-22 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='currencyconverter',
            old_name='base_currency',
            new_name='currency1',
        ),
        migrations.RenameField(
            model_name='currencyconverter',
            old_name='target_currency',
            new_name='currency2',
        ),
    ]
