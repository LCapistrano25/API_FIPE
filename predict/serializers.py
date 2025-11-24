from rest_framework import serializers

class PredictSerializer(serializers.Serializer):
    brand = serializers.CharField(max_length=100)
    model = serializers.CharField(max_length=100)
    fuel = serializers.CharField(max_length=100)
    gear = serializers.CharField(max_length=100)
    year = serializers.IntegerField()   
    engine = serializers.FloatField()

