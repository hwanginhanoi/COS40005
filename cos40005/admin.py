from .custom_view import SomeCustomView
from .models import Domain, Property, Cache
from django.contrib import admin
from django.http import HttpResponse, FileResponse
from django.urls import path
from django.shortcuts import redirect
import os
from .models import DataExport
from .helper import create_data, clean_data

from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule, SolarSchedule, ClockedSchedule


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

@admin.register(DataExport)
class DataExportAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'status')
    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('generate-csv/', self.generate_csv, name='generate-csv'),
            path('download-csv/', self.download_csv, name='download-csv'),
        ]
        return custom_urls + urls

    def generate_csv(self, request):
        try:
            # Create new export record
            export = DataExport.objects.create(status='processing')

            # Run your data generation functions
            create_data()
            clean_data()

            # Update export status
            export.status = 'completed'
            export.file_path = './output_cleaned.csv'
            export.save()

            self.message_user(request, "CSV file generated successfully!")
        except Exception as e:
            self.message_user(request, f"Error generating CSV: {str(e)}", level='ERROR')

        return redirect('admin:your_app_dataexport_changelist')

    def download_csv(self, request):
        try:
            file_path = './output_cleaned.csv'
            if os.path.exists(file_path):
                response = FileResponse(
                    open(file_path, 'rb'),
                    content_type='text/csv'
                )
                response['Content-Disposition'] = 'attachment; filename="output_cleaned.csv"'
                return response
            else:
                self.message_user(request, "CSV file not found. Generate it first.", level='ERROR')
        except Exception as e:
            self.message_user(request, f"Error downloading CSV: {str(e)}", level='ERROR')

        return redirect('admin:your_app_dataexport_changelist')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_generate_button'] = True
        extra_context['show_download_button'] = os.path.exists('./output_cleaned.csv')
        return super().changelist_view(request, extra_context=extra_context)

class CustomAdminSite(admin.AdminSite):
    site_header = "COS40005 Crawling Admin"
    site_title = "Admin Portal"
    index_title = "Welcome to the COS40005 Admin Portal"

    def get_urls(self):
        custom_urls = [
            path('dataexport/', self.admin_view(SomeCustomView.as_view(admin=self)), name='dataexport'),
        ]
        admin_urls = super().get_urls()
        return custom_urls + admin_urls


site = CustomAdminSite(name="my-fancy-url")
admin.site = site

site.register(Domain, DomainAdmin)
site.register(Cache, CacheAdmin)
site.register(Property, PropertyAdmin)
site.register(DataExport, DataExportAdmin)

site.register(PeriodicTask)
site.register(CrontabSchedule)
site.register(ClockedSchedule)

# admin.register....your...modeladmin
