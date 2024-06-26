# Generated by Django 5.0.6 on 2024-06-17 09:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('domain', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('area', models.DecimalField(decimal_places=2, max_digits=10)),
                ('floor', models.IntegerField()),
                ('bedroom', models.IntegerField()),
                ('toilet', models.IntegerField()),
                ('publish_date', models.DateField()),
                ('contact', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='cos40005.domain')),
            ],
        ),
    ]
