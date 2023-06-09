# Generated by Django 4.0.2 on 2023-06-05 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_remove_donation_food_items_donated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='food_items_donated',
            field=models.ManyToManyField(to='app1.FoodItem'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='stock',
            field=models.ManyToManyField(related_name='restaurants', to='app1.FoodItem'),
        ),
    ]
