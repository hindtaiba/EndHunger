# Generated by Django 4.0.2 on 2023-06-06 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_alter_donation_food_items_donated_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ngo',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
