from django.urls import path

from .views import (
    list_measurements,
    rud_measurement,
    download_measurement,
    save_to_mongo_measurement,
    filter_measurements
)

urlpatterns = [
    path('filters/', filter_measurements, name="filter_measurements"),
    path('measurements/', list_measurements, name="list_measurements"),
    path('measurement/download/', download_measurement, name="download_measurement"),
    path('measurement/save/', save_to_mongo_measurement, name="save_to_mongo_measurement"),
    path('measurement/<str:sample_id>/', rud_measurement, name="rud_measurement")
]
