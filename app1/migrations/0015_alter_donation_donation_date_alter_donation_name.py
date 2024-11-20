# Generated by Django 4.0.2 on 2023-06-18 19:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0014_alter_donation_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='donation_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='donation',
            name='name',
            field=models.CharField(editable=False, max_length=255, unique=True),
        ),
    ]