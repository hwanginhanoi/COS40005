from django.urls import path
from .views import API

urlpatterns = [
    path('load_data_address/', API.as_view(), name='myapi'),
]