from django.urls import path

from .views import list_create_device, rud_device

urlpatterns = [
    path('devices/', list_create_device, name="list_create_device"),
    path('device/<str:mac>/', rud_device, name="rud_device"),
]
