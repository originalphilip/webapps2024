# Generated by Django 5.0.3 on 2024-03-29 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0003_delete_transaction'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PaymentRequest',
        ),
    ]
