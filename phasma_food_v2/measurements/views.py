from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView

from .models import Measurement, Result
from .serializers import MeasurementSerializer, ResultSerializer


class CreateMeasurement(CreateAPIView):
    """Save measurement to DB."""
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def get_serializer_context(self) -> dict:
        """Add URL parameter in order to know if measurement
        will be analyzed.

        Returns:
            Context with additional key/value pair
        """
        context = super().get_serializer_context()
        if self.request:
            context.update(
                {
                    "operation": self.request.query_params.get("operation", "")
                }
            )
        return context


class RUDMeasurement(RetrieveUpdateDestroyAPIView):
    """Read/Update/Delete measurement."""
    queryset = Measurement.objects.all()
    lookup_field = "sample_id"
    serializer_class = MeasurementSerializer


class ListResult(ListAPIView):
    """List all results that are in DB."""
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


class RUDResult(RetrieveUpdateDestroyAPIView):
    """Read/Update/Delete result."""
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    lookup_field = "measurement_id"


create_measurement = CreateMeasurement.as_view()
rud_measurement = RUDMeasurement.as_view()
list_result = ListResult.as_view()
rud_result = RUDResult.as_view()

