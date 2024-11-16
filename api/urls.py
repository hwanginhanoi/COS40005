from django.urls import path
from .views import API, Summarize, RemoveOutlier, PriceDistribute, ProvinceDistribute, CorrelationMatrix

urlpatterns = [
    path('load_data_address/', API.as_view(), name='data_api'),
    path('data_analysis/summerize', Summarize.as_view(), name='summarize'),
    path('data_analysis/remove_outlier', RemoveOutlier.as_view(), name='remove_outlier'),
    path('data_analysis/price_distribution', PriceDistribute.as_view(), name='price_distribution'),
    path('data_analysis/province_distribution', ProvinceDistribute.as_view(), name='price_distribution'),
    path('data_analysis/correlation', CorrelationMatrix.as_view(), name='correlation'),
]