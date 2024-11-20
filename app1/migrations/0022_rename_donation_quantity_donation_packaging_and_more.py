# Generated by Django 4.0.2 on 2023-06-20 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0021_donation_donation_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donation',
            old_name='donation_quantity',
            new_name='packaging',
        ),
        migrations.AddField(
            model_name='donation',
            name='quantity',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='donation',
            name='transportation',
            field=models.CharField(default='', max_length=255),
        ),
    ]