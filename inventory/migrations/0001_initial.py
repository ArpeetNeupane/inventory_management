# Generated by Django 5.0.7 on 2024-11-10 11:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryName', models.CharField(max_length=30, unique=True)),
                ('categoryQuantity', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplierName', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=40)),
                ('contactNo', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemName', models.CharField(max_length=30, unique=True)),
                ('itemQuantity', models.PositiveIntegerField()),
                ('itemCode', models.PositiveIntegerField(editable=False, unique=True)),
                ('itemCategory', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.category')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectName', models.CharField(max_length=40)),
                ('projectLeader', models.CharField(max_length=30)),
                ('items', models.ManyToManyField(to='inventory.item')),
            ],
        ),
        migrations.CreateModel(
            name='SupplierItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField()),
                ('supply_date', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.item')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.supplier')),
            ],
        ),
        migrations.AddField(
            model_name='supplier',
            name='items',
            field=models.ManyToManyField(through='inventory.SupplierItem', to='inventory.item'),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('billNo', models.CharField(max_length=30, unique=True)),
                ('totalPrice', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('finalPriceWithVat', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.PositiveIntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.item')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.transaction')),
            ],
        ),
    ]
