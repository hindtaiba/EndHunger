# Generated by Django 4.0.2 on 2023-06-18 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0015_alter_donation_donation_date_alter_donation_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
