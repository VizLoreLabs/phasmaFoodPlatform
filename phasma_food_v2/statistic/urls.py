from django.urls import path

from .views import platformstatisticview

urlpatterns = [
    path('platform/<int:pk>/', platformstatisticview, name="platform"),
]
