# Generated by Django 5.0.7 on 2024-12-01 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_rename_paymentstate_transaction_paymentstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='paymentStatus',
            field=models.CharField(default='Pending', max_length=8),
        ),
    ]