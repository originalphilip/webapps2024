# Generated by Django 5.0.3 on 2024-05-01 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0019_paymentrequest_currency_alter_paymentrequest_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='points',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=1000, max_digits=10),
        ),
    ]