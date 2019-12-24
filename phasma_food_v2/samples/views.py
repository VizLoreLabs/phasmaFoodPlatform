from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from .mongo_db import MongoDB
from .serializers import RowSerializer, RowsSerializer


class Databases(APIView):
    """DBs that are in Mongo DB."""

    def get(self, request: HttpRequest) -> Response:
        return Response({"message": MongoDB().database_list()}, status=status.HTTP_200_OK)


class Collections(APIView):
    """Collections that are in Mongo for particular DB."""

    def get(self, request: HttpRequest, db: str) -> Response:
        return Response({"message": MongoDB().collection_list(db)}, status=status.HTTP_200_OK)


class Row(GenericAPIView):
    """Single document from Mongo DB."""
    serializer_class = RowSerializer

    def post(self, request: HttpRequest) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            request_data = serializer.validated_data
            mongo_data = MongoDB().find_row(**request_data)
            return Response({"message": mongo_data}, status=status.HTTP_200_OK)
        elif serializer.errors:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class Rows(GenericAPIView):
    """Multi documents from Mongo DB."""
    serializer_class = RowsSerializer

    def post(self, request: HttpRequest) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            request_data = serializer.validated_data

            data, data_query_total, data_total, page_num, page_size = MongoDB().find_rows(**request_data)
            number_of_pages = (data_total // page_size) + 1 if data_total % page_size else data_total // page_size
            context = {
                "total": data_total,
                "count": data_query_total,
                "number_of_pages": number_of_pages,
                "next": {"page_num": page_num + 1, "page_size": page_size} if page_num < number_of_pages else {},
                "previous": {"page_num": page_num + 1, "page_size": page_size} if 1 <= page_num - 1 <= number_of_pages else {},
                "results": data

            }

            return Response({"message": context}, status=status.HTTP_200_OK)

        elif serializer.errors:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


databases = Databases.as_view()
collections = Collections.as_view()
row = Row.as_view()
rows = Rows.as_view()
