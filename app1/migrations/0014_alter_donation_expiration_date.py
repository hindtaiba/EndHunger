# Generated by Django 4.0.2 on 2023-06-18 17:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0013_alter_donation_expiration_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='expiration_date',
            field=models.DateField(default=datetime.date(2023, 6, 21)),
        ),
    ]
