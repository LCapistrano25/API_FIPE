from fipe_car.views import EngineSizeFipeCarView, ModelFipeCarView, YearFipeCarView
from fipe_car.views import BrandFipeCarView
from fipe_car.views import FuelTypeFipeCarView
from fipe_car.views import GearTypeFipeCarView
from django.urls import path
from fipe_car.views import FipeCarView

urlpatterns = [
    path('car/', FipeCarView.as_view(), name='fipe_car'),
    path('car/models/', ModelFipeCarView.as_view(), name='fipe_car_models'),
    path('car/brands/', BrandFipeCarView.as_view(), name='fipe_car_brands'),
    path('car/fuel_types/', FuelTypeFipeCarView.as_view(), name='fipe_car_fuel_types'),
    path('car/gear_types/', GearTypeFipeCarView.as_view(), name='fipe_car_gear_types'),
    path('car/years/', YearFipeCarView.as_view(), name='fipe_car_years'),
    path('car/engine_sizes/', EngineSizeFipeCarView.as_view(), name='fipe_car_engine_sizes'),
]