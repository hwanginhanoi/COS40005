from .models import Domain, Property
from django.contrib import admin
from django_celery_beat.models import PeriodicTask, CrontabSchedule


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('title', 'domain')


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'price', 'area', 'floor', 'bedroom', 'toilet', 'publish_date', 'contact')
    list_filter = ('domain', 'publish_date')
    search_fields = ('title', 'address', 'contact')

