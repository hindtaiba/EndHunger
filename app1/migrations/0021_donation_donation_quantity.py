# Generated by Django 4.0.2 on 2023-06-20 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0020_ngo_profile_picture_restaurant_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='donation_quantity',
            field=models.CharField(default='', max_length=255),
        ),
    ]