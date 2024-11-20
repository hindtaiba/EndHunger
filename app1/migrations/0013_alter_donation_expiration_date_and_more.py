# Generated by Django 4.2.1 on 2023-06-17 11:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0012_donation_requested_alter_donation_expiration_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='expiration_date',
            field=models.DateField(default=datetime.date(2023, 6, 20)),
        ),
        migrations.DeleteModel(
            name='DonationRequest',
        ),
    ]
