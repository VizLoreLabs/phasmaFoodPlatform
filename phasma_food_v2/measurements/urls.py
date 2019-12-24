from django.urls import path

from .views import create_measurement, rud_measurement, rud_result, list_result

urlpatterns = [
    path('measurement/create/', create_measurement, name="create_measurement"),
    path('measurement/<str:sample_id>/', rud_measurement, name="rud_measurement"),
    path('results/', list_result, name="list_results"),
    path('result/<str:measurement_id>/', rud_result, name="rud_result"),
]
