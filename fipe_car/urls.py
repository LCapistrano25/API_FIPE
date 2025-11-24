from django.urls import path
from fipe_car.views import FipeCarView

urlpatterns = [
    path('car/', FipeCarView.as_view(), name='fipe_car'),
]