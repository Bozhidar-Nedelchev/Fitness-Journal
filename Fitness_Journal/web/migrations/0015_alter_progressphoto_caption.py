# Generated by Django 4.2.3 on 2023-08-18 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0014_mealplan_mealentry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progressphoto',
            name='caption',
            field=models.CharField(max_length=30),
        ),
    ]