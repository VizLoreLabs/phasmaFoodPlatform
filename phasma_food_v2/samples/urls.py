from django.urls import path

from .views import row, rows, databases, collections

urlpatterns = [
    path('databases/', databases, name="databases"),
    path('collections/<str:db>/', collections, name="collections"),
    path('row/', row, name="row"),
    path('rows/', rows, name="rows"),
]
