# Generated by Django 5.0.6 on 2024-07-08 07:23

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
                ('name', models.CharField(max_length=255)),
                ('domain', models.CharField(max_length=255)),
                ('title_type', models.CharField(blank=True, choices=[('By.XPATH', 'XPath'), ('By.CLASS_NAME', 'Classname'), ('By.CSS_SELECTOR', 'CSS Selector'), ('By.NAME', 'Name'), ('By.ID', 'ID')], max_length=20, null=True)),
                ('title_property', models.CharField(default='', max_length=255)),
                ('address_type', models.CharField(blank=True, choices=[('By.XPATH', 'XPath'), ('By.CLASS_NAME', 'Classname'), ('By.CSS_SELECTOR', 'CSS Selector'), ('By.NAME', 'Name'), ('By.ID', 'ID')], max_length=20, null=True)),
                ('address_property', models.CharField(default='', max_length=255)),
                ('price_type', models.CharField(blank=True, choices=[('By.XPATH', 'XPath'), ('By.CLASS_NAME', 'Classname'), ('By.CSS_SELECTOR', 'CSS Selector'), ('By.NAME', 'Name'), ('By.ID', 'ID')], max_length=20, null=True)),
                ('price_property', models.CharField(default='', max_length=255)),
                ('area_type', models.CharField(blank=True, choices=[('By.XPATH', 'XPath'), ('By.CLASS_NAME', 'Classname'), ('By.CSS_SELECTOR', 'CSS Selector'), ('By.NAME', 'Name'), ('By.ID', 'ID')], max_length=20, null=True)),
                ('area_property', models.CharField(default='', max_length=255)),
                ('floor_type', models.CharField(blank=True, choices=[('By.XPATH', 'XPath'), ('By.CLASS_NAME', 'Classname'), ('By.CSS_SELECTOR', 'CSS Selector'), ('By.NAME', 'Name'), ('By.ID', 'ID')], max_length=20, null=True)),
                ('floor_property', models.CharField(default='', max_length=255)),
                ('bedroom_type', models.CharField(blank=True, choices=[('By.XPATH', 'XPath'), ('By.CLASS_NAME', 'Classname'), ('By.CSS_SELECTOR', 'CSS Selector'), ('By.NAME', 'Name'), ('By.ID', 'ID')], max_length=20, null=True)),
                ('bedroom_property', models.CharField(default='', max_length=255)),
                ('toilet_type', models.CharField(blank=True, choices=[('By.XPATH', 'XPath'), ('By.CLASS_NAME', 'Classname'), ('By.CSS_SELECTOR', 'CSS Selector'), ('By.NAME', 'Name'), ('By.ID', 'ID')], max_length=20, null=True)),
                ('toilet_property', models.CharField(default='', max_length=255)),
                ('publish_date_type', models.CharField(blank=True, choices=[('By.XPATH', 'XPath'), ('By.CLASS_NAME', 'Classname'), ('By.CSS_SELECTOR', 'CSS Selector'), ('By.NAME', 'Name'), ('By.ID', 'ID')], max_length=20, null=True)),
                ('publish_date_property', models.CharField(default='', max_length=255)),
                ('contact_type', models.CharField(blank=True, choices=[('By.XPATH', 'XPath'), ('By.CLASS_NAME', 'Classname'), ('By.CSS_SELECTOR', 'CSS Selector'), ('By.NAME', 'Name'), ('By.ID', 'ID')], max_length=20, null=True)),
                ('contact_property', models.CharField(default='', max_length=255)),
                ('description_type', models.CharField(blank=True, choices=[('By.XPATH', 'XPath'), ('By.CLASS_NAME', 'Classname'), ('By.CSS_SELECTOR', 'CSS Selector'), ('By.NAME', 'Name'), ('By.ID', 'ID')], max_length=20, null=True)),
                ('description_property', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Cache',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=False)),
                ('visited', models.BooleanField(default=False)),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='caches', to='cos40005.domain')),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('price', models.CharField(max_length=255)),
                ('area', models.CharField(max_length=255)),
                ('floor', models.CharField(max_length=255)),
                ('bedroom', models.CharField(max_length=255)),
                ('toilet', models.CharField(max_length=255)),
                ('publish_date', models.CharField(max_length=255)),
                ('contact', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='cos40005.domain')),
            ],
        ),
    ]
