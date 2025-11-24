from django.urls import path
from . import views

urlpatterns = [
    path('car/', views.PredictAPIView.as_view(), name='predict'),
]
