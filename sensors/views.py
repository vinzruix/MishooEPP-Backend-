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
from sensors.services import ping_url, create_user_node, create_sensor_node, send_server_credentials, get_sensor_node, \
    create_all_sensor_data


# Create your views here.

class SensorNodeObtainPairSerializerAPIView(TokenObtainPairView):
    serializer_class = SensorNodeObtainPairSerializer


class SensorNodeListCreateAPIView(APIView):

    def get_permissions(self):
        if self.request.method == "POST":
            return [permission_required("sensors.create_sensor")()]

        if self.request.method == "PUT":
            return [permission_required("sensors.create_sensor")()]

        if self.request.method == "GET":
            return [permission_required("sensors.view_all_sensor")()]
        return [IsAuthenticated()]

    @staticmethod
    def post(request):

        try:
            node = {
                "name": request.data["name"],
                "department": request.data["department"],
                "ip": request.data["ip"],
            }

        except MultiValueDictKeyError as e:
            raise NotAcceptable({"error": f"value missing {e}"})

        with transaction.atomic():
            try:
                node_username = uuid.uuid4()
                node_password = secrets.token_urlsafe(16)
                node_user = create_user_node(node_username, node_password)
                create_sensor_node(node["name"], node["department"], node["ip"], node_user)

                def send_credentials_safe():
                    try:
                        send_server_credentials(node_username, node_password, node["ip"], request.get_port())
                    except ValueError:
                        print("Error enviando credenciales")

                transaction.on_commit(send_credentials_safe)

            except ValueError:
                raise NotAcceptable()

        return Response({"success": f"Sensor creado"}, status=status.HTTP_201_CREATED)


    @staticmethod
    def get(request):
        node_data = SensorNode.objects.all().order_by("-id")
        serializer = SensorNodeSerializer(node_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SensorNodeDetailPatchAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [permission_required("sensors.view_all_sensor")()]

        if self.request.method == "patch":
            return [permission_required("sensors.create_sensor")()]
        return [IsAuthenticated()]

    @staticmethod
    def get(request, sensor_node_id):

        try:
            node_data = get_sensor_node(sensor_node_id)
        except Exception as e:
            raise NotAcceptable({"error": f"{e}"})

        serializer = SensorNodeSerializer(node_data, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def patch(request, sensor_node_id):
        try:
            node_data = get_sensor_node(sensor_node_id)
        except Exception as e:
            raise NotAcceptable({"error": f"{e}"})

        serializer = SensorNodeSerializer(instance=node_data, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

        if not serializer.is_valid():
            raise NotAcceptable()

        instance = serializer.instance
        node_password = secrets.token_urlsafe(16)
        instance.sensor_user.set_password(node_password)

        try:
            send_server_credentials(instance.sensor_user.username, node_password, instance.sensor_user.ip,
                                    request.get_port())
        except ValueError as e:
            raise NotAcceptable(f"{e}")

        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, sensor_node_id):
        try:
            sensor_node = get_sensor_node(sensor_node_id)
        except Exception as e:
            raise NotAcceptable({"error": f"{e}"})

        sensor_node.delete()

        return Response({"success": f"{sensor_node.id} eliminated"}, status.HTTP_200_OK)


class SensorsDataCreateAPIView(APIView):

    def get_permissions(self):

        if self.request.method == "POST":
            return [permission_required("sensors.create_data_sensor")()]

        return [IsAuthenticated()]

    @staticmethod
    def post(request):
        try:
            create_all_sensor_data(
                request.user,
                request.POST["temp"],
                request.POST["hum"],
                request.POST["eco2"],
                request.POST["tvoc"],
            )
        except Exception as e:
            raise NotAcceptable({"error": f"{e}"})

        return Response({"success": "Data saved"}, status=status.HTTP_201_CREATED)


class SensorDataDetailAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [permission_required("sensors.view_all_sensor")()]

        return [IsAuthenticated()]

    @staticmethod
    def get(request, sensor_node_id):

        try:
            node_data = SensorNode.objects.get(id=sensor_node_id)
        except Exception as e:
            raise NotAcceptable({"error": f"{e}"})

        serializer = SensorDataSerializer(node_data, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
