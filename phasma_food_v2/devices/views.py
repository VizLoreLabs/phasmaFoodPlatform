from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from .models import PhasmaDevice
from .serializers import PhasmaDeviceSerializer


class ListCPhasmaDevice(ListCreateAPIView):
    """List/Create phasma device/s."""
    queryset = PhasmaDevice.objects.all()
    serializer_class = PhasmaDeviceSerializer


class RUDPhasmaDevice(RetrieveUpdateDestroyAPIView):
    """Read/Update/Delete phasma device."""
    queryset = PhasmaDevice.objects.all()
    serializer_class = PhasmaDeviceSerializer
    lookup_field = "mac"


list_create_device = ListCPhasmaDevice.as_view()
rud_device = RUDPhasmaDevice.as_view()
