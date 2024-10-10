from .models import Domain, Property, Cache
from django.contrib import admin


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'domain', 'title_type', 'title_property',
        'address_type', 'address_property', 'price_type', 'price_property',
        'area_type', 'area_property', 'floor_type', 'floor_property',
        'bedroom_type', 'bedroom_property', 'toilet_type', 'toilet_property',
        'publish_date_type', 'publish_date_property', 'contact_type', 'contact_property',
        'description_type', 'description_property'
    ]
    fieldsets = (
        (None, {
            'fields': ('name', 'domain', 'enable')
        }),
        ('Title Information', {
            'fields': ('title_type', 'title_property')
        }),
        ('Address Information', {
            'fields': ('address_type', 'address_property')
        }),
        ('Price Information', {
            'fields': ('price_type', 'price_property')
        }),
        ('Area Information', {
            'fields': ('area_type', 'area_property')
        }),
        ('Floor Information', {
            'fields': ('floor_type', 'floor_property')
        }),
        ('Bedroom Information', {
            'fields': ('bedroom_type', 'bedroom_property')
        }),
        ('Toilet Information', {
            'fields': ('toilet_type', 'toilet_property')
        }),
        ('Publish Date Information', {
            'fields': ('publish_date_type', 'publish_date_property')
        }),
        ('Contact Information', {
            'fields': ('contact_type', 'contact_property')
        }),
        ('Description Information', {
            'fields': ('description_type', 'description_property')
        }),
    )
    search_fields = ['name', 'domain']
    list_filter = ['title_type', 'address_type', 'price_type', 'area_type', 'floor_type', 'bedroom_type', 'toilet_type',
                   'publish_date_type', 'contact_type', 'description_type']


@admin.register(Cache)
class CacheAdmin(admin.ModelAdmin):
    list_display = ('domain', 'url', 'status', 'visited')


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'price', 'area', 'floor', 'bedroom', 'toilet', 'publish_date', 'contact', 'description')
    list_filter = ('domain', 'publish_date')
    search_fields = ('title', 'address', 'contact')
