from fipe_car.pagination import FipeCarPagination
from fipe_car.models import FipeCar
from fipe_car.serializers import FipeCarSerializer
from rest_framework.generics import ListAPIView

class FipeCarView(ListAPIView):
    queryset = FipeCar.objects.all()
    serializer_class = FipeCarSerializer
    pagination_class = FipeCarPagination