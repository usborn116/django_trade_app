# Generated by Django 5.0 on 2023-12-24 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='s2',
            field=models.CharField(default=None, max_length=2000),
        ),
        migrations.AddField(
            model_name='league',
            name='sw',
            field=models.CharField(default=None, max_length=2000),
        ),
    ]
