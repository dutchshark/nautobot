# Generated by Django 3.1.14 on 2021-12-21 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcim', '0008_increase_length_of_device_serial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryitem',
            name='serial',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='rack',
            name='serial',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]