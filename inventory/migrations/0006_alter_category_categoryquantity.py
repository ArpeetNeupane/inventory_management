# Generated by Django 5.0.7 on 2024-12-20 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_rename_project_projectitem_associated_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='categoryQuantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
