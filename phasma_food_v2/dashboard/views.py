import os
import mimetypes
from wsgiref.util import FileWrapper
from typing import Union

from django.http import StreamingHttpResponse, HttpRequest
from django.conf import settings
from rest_framework import generics, status, views
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from phasma_food_v2.measurements.models import Measurement
from phasma_food_v2.measurements.serializers import MeasurementSerializer
from phasma_food_v2.samples.mongo_db import MongoDB

from .serializers import MeasurementDownloadSerializer, MeasurementMongoSerializer, ListMeasurementSerializer
from .tasks import create_excel_to_zip, save_to_mongo
from .utils import excel_zip


class FilterMeasurements(views.APIView):
    """Distinct values for useCase and foodType."""

    def get(self, request: HttpRequest) -> Response:
        queryset = Measurement.objects.all()
        use_cases = queryset.order_by().values_list('use_case', flat=True).distinct()
        food_types = queryset.order_by().values_list('food_type', flat=True).distinct()
        uc_ft = {
            use_case: queryset.filter(use_case=use_case).order_by().values_list('food_type', flat=True).distinct()
            for use_case in use_cases
        }
        data = {
            "use_case": use_cases,
            "food_type": food_types,
            "uc_ft": uc_ft
        }

        return Response({"filter": data}, status=status.HTTP_200_OK)


class ListMeasurements(generics.ListAPIView):
    """Measurements list that are in DB.
    Fields that filters can be applied on:
      - useCase
      - foodType
    """
    queryset = Measurement.objects.all()
    serializer_class = ListMeasurementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["use_case", "food_type"]
    ordering = ["-date_created"]


class RUDMeasurement(generics.RetrieveUpdateDestroyAPIView):
    """Read/Update/Delete measurement by Measurement ID."""
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    lookup_field = "sample_id"


class MeasurementDownload(generics.GenericAPIView):
    """Generate excel file/s, zip and send them
    via email and download thru browser.
    """
    serializer_class = MeasurementDownloadSerializer

    def post(self, request: HttpRequest) -> Union[StreamingHttpResponse, Response]:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            measurements = serializer.validated_data.get("measurements")
            email = request.user
            full_folder_path, folder_name = excel_zip(
                email=email.email,
                measurements=measurements
            )
            zip_file = "{}/{}.zip".format(
                full_folder_path,
                folder_name.replace(".", "")
            )
            chunk_size = 8192
            response = StreamingHttpResponse(
                FileWrapper(open(zip_file, 'rb'), chunk_size),
                content_type=mimetypes.guess_type(zip_file)[0]
            )
            response['Content-Length'] = os.path.getsize(zip_file)
            response['Content-Disposition'] = "attachment; filename={}.zip".format(folder_name.replace(".", ""))
            create_excel_to_zip.delay(
                email=email.email,
                measurements=measurements
            )
            return response

        elif serializer.errors:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class MeasurementMongo(generics.GenericAPIView):
    """Save measurement from Postgres to Mongo DB bu Measurement ID."""
    serializer_class = MeasurementMongoSerializer

    def get(self, request: HttpRequest) -> Response:
        mongo_client = MongoDB()
        dbs = mongo_client.database_list()
        mongo_dict = {}
        for db in dbs:
            collections = mongo_client.collection_list(db)
            collections_dict = {}
            if collections:
                for collection in collections:
                    collections_dict[collection] = mongo_client.counter(
                        item={},
                        collection=collection
                    )
            mongo_dict[db] = collections_dict

        return Response({"db_collections": mongo_dict}, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            measurements = serializer.validated_data.get("measurements")
            db = serializer.validated_data.get("db", settings.MONGO_DEFAULT_DB)
            collection = serializer.validated_data.get("collection", settings.MONGO_DEFAULT_COLLECTION)
            email = request.user
            save_to_mongo.delay(
                db=db,
                collection=collection,
                measurements=measurements
            )
            return Response({"message": "Processing request by {}. Phasma Food Team.".format(email)},
                            status=status.HTTP_200_OK)

        elif serializer.errors:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


list_measurements = ListMeasurements.as_view()
rud_measurement = RUDMeasurement.as_view()
download_measurement = MeasurementDownload.as_view()
save_to_mongo_measurement = MeasurementMongo.as_view()
filter_measurements = FilterMeasurements.as_view()
