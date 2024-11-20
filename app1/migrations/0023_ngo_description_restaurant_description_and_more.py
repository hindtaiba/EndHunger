# Generated by Django 4.2.1 on 2023-06-24 08:54

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0022_rename_donation_quantity_donation_packaging_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ngo',
            name='description',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='description',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='donation',
            name='expiration_date',
            field=models.DateField(default=datetime.date(2023, 6, 27)),
        ),
        migrations.AlterField(
            model_name='donation',
            name='ngo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='donations_received', to='app1.ngo'),
        ),
        migrations.AlterField(
            model_name='ngo',
            name='capacity',
            field=models.CharField(max_length=20),
        ),
    ]