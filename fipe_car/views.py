from fipe_car.pagination import FipeCarPagination, GenericPagination
from fipe_car.models import FipeCar
from fipe_car.serializers import FipeCarSerializer
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

class FipeCarView(ListAPIView):
    queryset = FipeCar.objects.all()
    serializer_class = FipeCarSerializer
    pagination_class = FipeCarPagination

class BaseDistinctListView(APIView):
    field_name = None   # definir nas subclasses

    def get(self, request):
        if not self.field_name:
            return Response({"error": "field_name not configured"}, status=500)

        pagination = GenericPagination()

        queryset = (
            FipeCar.objects
            .values_list(self.field_name, flat=True)
            .distinct()
            .order_by(self.field_name)
        )

        paginated = pagination.paginate_queryset(queryset, request)

        return pagination.get_paginated_response(list(paginated))

class ModelFipeCarView(BaseDistinctListView):
    field_name = "model"

class BrandFipeCarView(BaseDistinctListView):
    field_name = "brand"

class FuelTypeFipeCarView(BaseDistinctListView):
    field_name = "fuel_type"

class GearTypeFipeCarView(BaseDistinctListView):
    field_name = "gear_type"
