from django.utils import timezone
from predict.serializers import PredictSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .model_loader import model_random_forest_regressor, encoder_brand, encoder_fuel, encoder_model, encoder_gear
import numpy as np

class PredictAPIView(APIView):
    serializer_class = PredictSerializer
    
    def post(self, request):
        data = request.data

        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        brand_encoded = encoder_brand.transform([data["brand"]])[0]
        model_encoded = encoder_model.transform([data["model"]])[0]
        fuel_encoded = encoder_fuel.transform([data["fuel"]])[0]
        gear_encoded = encoder_gear.transform([data["gear"]])[0]

        year_use =  timezone.now().year - int(data["year"])
        
        input = np.array([[
            data["year"],
            year_use,
            data["engine"],
            brand_encoded,
            model_encoded,
            fuel_encoded,
            gear_encoded,
        ]])
        
        predict = model_random_forest_regressor.predict(input)
        return Response({"prediction": float(predict[0])})
