# Generated by Django 5.0.7 on 2024-12-01 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_remove_item_itemcode_individualitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='paymentState',
            field=models.CharField(default='pending', max_length=8),
        ),
    ]
