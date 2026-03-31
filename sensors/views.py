from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from MishooEPP_Backend.permissions import permission_required
from sensors.models import Temperature, Humidity, CO2, TVOC, Pressure
from sensors.serializers import TemperatureSerializer, HumiditySerializer, PressureSerializer, CO2Serializer, \
    TVOCSerializer


# Create your views here.

class SensorsCreateAPIView(APIView):

    def post(self, request):
        temp_value = request.POST['temp']
        hum_value = request.POST['hum']
        #press_value = request.POST["press"]
        co2_value = request.POST["eco2"]
        tvoc_value = request.POST["tvoc"]

        Temperature.objects.create(value=temp_value)
        Humidity.objects.create(value=hum_value)
        CO2.objects.create(value=co2_value)
        TVOC.objects.create(value=tvoc_value)

        return Response(status=status.HTTP_201_CREATED)


class BaseSensorListAPIView(APIView):

    permission_classes = [permission_required('sensors.view_all_sensor')]
    model = None
    serializer_class = None

    def get(self,request):
        last_10_register = self.model.objects.order_by("-date")[:10]
        serializer = self.serializer_class(last_10_register, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TemperatureListAPIView(BaseSensorListAPIView):
    model = Temperature
    serializer_class = TemperatureSerializer

class HumidityListAPIView(BaseSensorListAPIView):
    model = Humidity
    serializer_class = HumiditySerializer

class PressureListAPIView(BaseSensorListAPIView):
    model = Pressure
    serializer_class = PressureSerializer

class CO2ListAPIView(BaseSensorListAPIView):
    model = CO2
    serializer_class = CO2Serializer

class TVOCListAPIView(BaseSensorListAPIView):
    model = TVOC
    serializer_class = TVOCSerializer


