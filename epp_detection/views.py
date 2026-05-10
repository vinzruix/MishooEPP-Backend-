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
from scipy.linalg import rq

from MishooEPP_Backend.permissions import permission_required
from epp_detection.models import EPPNode
from epp_detection.serializers import EPPNodeObtainPairSerializer, EPPNodeSerializer
from epp_detection.services import create_epp_node, get_epp_node, send_server_credentials
from sensors.services import create_user_node, create_sensor_node


# Create your views here.

class EPPNodeObtainPairSerializerAPIView(TokenObtainPairView):
    serializer_class = EPPNodeObtainPairSerializer


class EPPNodeListCreateAPIView(APIView):

    def get_permissions(self):
        if self.request.method == "POST":
            return [permission_required("sensors.create_sensor")()]
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

        node_user = False
        new_node = False

        try:

            node_username = uuid.uuid4()
            node_password = secrets.token_urlsafe(16)
            node_user = create_user_node(node_username, node_password)
            new_node = create_sensor_node(node["name"], node["department"], node["ip"], node_user)

            send_server_credentials(node_username, node_password, node["ip"], request.get_port(), request.auth)

        except ValueError as e:
            if node_user:
                node_user.delete()

            if new_node:
                node_user.delete()

            raise NotAcceptable(f"{e}")

        return Response({"success": f"Sensor creado"}, status=status.HTTP_201_CREATED)

    @staticmethod
    def get(request):
        node_data = EPPNode.objects.all().order_by("-id")
        serializer = EPPNodeSerializer(node_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EPPNodeDetailPatchDeleteAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [permission_required("sensors.view_all_sensor")()]

        if self.request.method == "patch":
            return [permission_required("sensors.create_sensor")()]

        if self.request.method == "delete":
            return [permission_required("sensors.create_sensor")()]
        return [IsAuthenticated()]

    @staticmethod
    def get(request, epp_node_id):

        try:
            node_data = get_epp_node(epp_node_id)
        except Exception as e:
            raise NotAcceptable({"error": f"{e}"})

        serializer = EPPNodeSerializer(node_data, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def patch(request, epp_node_id):
        try:
            node_data = get_epp_node(epp_node_id)
        except Exception as e:
            raise NotAcceptable({"error": f"{e}"})

        serializer = EPPNodeSerializer(instance=node_data, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

        if not serializer.is_valid():
            raise NotAcceptable()

        instance = serializer.instance
        node_password = secrets.token_urlsafe(16)
        instance.sensor_user.set_password(node_password)

        try:
            send_server_credentials(instance.sensor_user.username, node_password, instance.sensor_user.ip,
                                    request.get_port(), request.auth)
        except ValueError as e:
            raise NotAcceptable(f"{e}")

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete(request, epp_node_id):
        try:
            sensor_node = get_epp_node(epp_node_id)
        except Exception as e:
            raise NotAcceptable({"error": f"{e}"})

        sensor_node.delete()

        return Response({"success": f"{sensor_node.id} eliminated"}, status.HTTP_200_OK)
