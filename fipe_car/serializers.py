from rest_framework import serializers

from fipe_car.models import FipeCar

class FipeCarSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FipeCar
        fields = [
            'fipe_id',
            'brand',
            'model',
            'year',
            'fuel_type',
            'gear_type',
            'engine_size',
            'price',
        ]