# Generated by Django 5.0.6 on 2024-07-09 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cos40005', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cache',
            name='url',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='domain',
            name='domain',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]