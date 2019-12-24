from django.contrib.auth import get_user_model
from rest_framework import generics

from .serializers import PlatformStatisticSerializer
from .models import PlatformStatistic

User = get_user_model()


class PlatformStatisticView(generics.RetrieveAPIView):
    """Get statistic (users, phasma_device, mobile,
    use case, food type, total measurements, machine learning models)
    for PhasmaFood platform.
    """
    queryset = PlatformStatistic.objects.all()
    serializer_class = PlatformStatisticSerializer


platformstatisticview = PlatformStatisticView.as_view()
