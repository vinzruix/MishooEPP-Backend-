import secrets
import uuid
from django.db import transaction
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.exceptions import NotAcceptable
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from MishooEPP_Backend.permissions import permission_required
from sensors.models import Temperature, Humidity, CO2, TVOC, Pressure, SensorNode
from sensors.serializers import TemperatureSerializer, HumiditySerializer, PressureSerializer, CO2Serializer, \
    TVOCSerializer, SensorNodeObtainPairSerializer, SensorNodeSerializer, SensorDataSerializer
from sensors.services import ping_url, create_user_node, create_sensor_node, send_server_credentials


# Create your views here.

class SensorNodeObtainPairSerializerAPIView(TokenObtainPairView):
    serializer_class = SensorNodeObtainPairSerializer


class SensorNodeCreateAPIView(APIView):

    def get_permissions(self):
        if self.request == "POST":
            return [permission_required("sensors.create_sensor")()]

        if self.request == "GET":
            return [permission_required("sensors.view_all_sensor")()]
        return [IsAuthenticated()]


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
           #     ping_url(node["ip"])

                node_username = uuid.uuid4()
                node_password = secrets.token_urlsafe(16)

                node_user = create_user_node(node_username, node_password)

                create_sensor_node(request.data["name"], request.data["location"], request.data["ip"], node_user)

                send_server_credentials(node_username, node_password, request.data["ip"])

        except ValueError as e:
            raise NotAcceptable({"error":f"{e}"})
            

        return Response({"success": f"Sensor creado"})

    def get(self,request):
        node_data = SensorNode.objects.last()
        serializer = SensorNodeSerializer(node_data,many=False)
        return Response(serializer.data)


class SensorsDataCreateAPIView(APIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return [permission_required("sensors.view_all_sensor")()]

        if self.request.method == "POST":
            return [permission_required("sensors.create_sensor")()]

        return [IsAuthenticated()]

    def post(self, request):
        temp_value = request.POST['temp']
        hum_value = request.POST['hum']
        # press_value = request.POST["press"]
        co2_value = request.POST["eco2"]
        tvoc_value = request.POST["tvoc"]


        try:
            with transaction.atomic():

                Temperature.objects.create(value=temp_value, node=request.user.sensor_nodes)
                Humidity.objects.create(value=hum_value, node=request.user.sensor_nodes)
                CO2.objects.create(value=co2_value, node=request.user.sensor_nodes)
                TVOC.objects.create(value=tvoc_value, node=request.user.sensor_nodes)

        except Exception as e:
            raise NotAcceptable({"error":f"{e}"})

        return Response(status=status.HTTP_201_CREATED)



class SensorDataDetailAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [permission_required("sensors.view_all_sensor")()]

        return [IsAuthenticated()]

    def get(self,request,sensor_node):

        try:
            node_data = SensorNode.objects.get(id=sensor_node)
        except Exception as e:
            raise NotAcceptable({"error":f"{e}"})


        serializer = SensorDataSerializer(node_data,many=False)
        return Response(serializer.data)


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
