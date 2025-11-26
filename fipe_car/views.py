from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from fipe_car.pagination import FipeCarPagination, GenericPagination
from fipe_car.models import FipeCar
from fipe_car.serializers import FipeCarSerializer
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

class FipeCarView(ListAPIView):
    queryset = FipeCar.objects.all()
    serializer_class = FipeCarSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['model', 'brand', 'fuel_type', 'gear_type', 'year', 'engine_size', 'fipe_id']
    ordering_fields = ['price', 'year', 'engine_size']
    pagination_class = FipeCarPagination

class BaseDistinctListView(APIView):
    field_name = None   # definir nas subclasses
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['model', 'brand', 'fuel_type', 'gear_type']
    pagination_class = GenericPagination
    
    def get(self, request):
        if not self.field_name:
            return Response({"error": "field_name not configured"}, status=500)

        pagination = self.pagination_class()

        base = FipeCar.objects.all()
        q = request.query_params.get("q")
        if q:
            base = base.filter(**{f"{self.field_name}__icontains": q})

        if self.field_name == "model":
            brand = request.query_params.get("brand")
            if brand:
                base = base.filter(brand__icontains=brand)

        if self.field_name == "fuel_type":
            brand = request.query_params.get("brand")
            model = request.query_params.get("model")
            if brand:
                base = base.filter(brand__icontains=brand)
            if model:
                base = base.filter(model__icontains=model)

        if self.field_name == "gear_type":
            brand = request.query_params.get("brand")
            model = request.query_params.get("model")
            if brand:
                base = base.filter(brand__icontains=brand)
            if model:
                base = base.filter(model__icontains=model)

        if self.field_name == "year":
            brand = request.query_params.get("brand")
            model = request.query_params.get("model")
            if brand:
                base = base.filter(brand__icontains=brand)
            if model:
                base = base.filter(model__icontains=model)
                
        if self.field_name == "engine_size":
            brand = request.query_params.get("brand")
            model = request.query_params.get("model")
            if brand:
                base = base.filter(brand__icontains=brand)
            if model:
                base = base.filter(model__icontains=model)
                
        queryset = (
            base
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

class YearFipeCarView(BaseDistinctListView):
    field_name = "year"

class EngineSizeFipeCarView(BaseDistinctListView):
    field_name = "engine_size"
