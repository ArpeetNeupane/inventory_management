# Generated by Django 5.0.7 on 2024-12-08 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_alter_transactionitem_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionitem',
            name='price',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='transactionitem',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
    ]
