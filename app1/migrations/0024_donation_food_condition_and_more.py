# Generated by Django 4.0.2 on 2023-06-24 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0023_ngo_description_restaurant_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='food_condition',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='donation',
            name='expiration_date',
            field=models.CharField(default='', max_length=255),
        ),
    ]
