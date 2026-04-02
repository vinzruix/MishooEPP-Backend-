import secrets
import uuid
from django.db import transaction
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.exceptions import NotAcceptable
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from MishooEPP_Backend.permissions import permission_required
from sensors.models import Temperature, Humidity, CO2, TVOC, Pressure
from sensors.serializers import TemperatureSerializer, HumiditySerializer, PressureSerializer, CO2Serializer, \
    TVOCSerializer, SensorNodeObtainPairSerializer
from sensors.services import ping_url, create_user_node, create_sensor_node, send_server_credentials


# Create your views here.

class SensorNodeObtainPairSerializerAPIView(TokenObtainPairView):
    serializer_class = SensorNodeObtainPairSerializer


class SensorNodeCreateAPIView(APIView):

    def post(self, request):
        
        try:
            node = {
                "name": request.data["name"],
                "location": request.data["location"],
                "ip": request.data["ip"],
            }

        except MultiValueDictKeyError as e:
            raise NotAcceptable({"error":f"value missing {e}"})


        try:
            with transaction.atomic():
                ping_url(node["ip"])

                node_username = uuid.uuid4()
                node_password = secrets.token_urlsafe(16)

                node_user = create_user_node(node_username, node_password)

                create_sensor_node(request.data["name"], request.data["location"], request.data["ip"], node_user)

                send_server_credentials(node_username, node_password, request.data["ip"])

        except ValueError as e:
            raise NotAcceptable({"error":f"{e}"})
            

        return Response({"success": f"{node_password}"})


class SensorsCreateAPIView(APIView):

    def post(self, request):
        temp_value = request.POST['temp']
        hum_value = request.POST['hum']
        # press_value = request.POST["press"]
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

    def get(self, request):
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
