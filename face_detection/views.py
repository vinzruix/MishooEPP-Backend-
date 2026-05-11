import secrets
import uuid
from django.db import transaction
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.exceptions import NotAcceptable
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from MishooEPP_Backend.exeptions import ObjectDoesNotExist, ObjectAlreadyExists, ServerDown, ServerBadResponse
from MishooEPP_Backend.permissions import permission_required
from MishooEPP_Backend.sensor_factories import CameraNodeCreator
from face_detection.models import CameraNode
from face_detection.serializers import CameraNodeObtainPairSerializer, CameraNodeSerializer
from face_detection.services import create_camera_node, send_server_credentials
from sensors.services import create_user_node


class CameraNodeObtainPairSerializerAPIView(TokenObtainPairView):
    serializer_class = CameraNodeObtainPairSerializer


class CameraNodeViewSet(ViewSet):

    def get_permissions(self):
        if self.action == "create":
            return [permission_required("sensors.create_sensor")()]

        if self.action == "partial_update":
            return [permission_required("sensors.create_sensor")()]

        if self.action == "destroy":
            return [permission_required("sensors.create_sensor")()]
        return [IsAuthenticated()]

    # noinspection PyUnboundLocalVariable
    @staticmethod
    def create(request):
        try:

            node = {
                "name": request.data["name"],
                "department": request.data["department"],
                "ip": request.data["ip"],
            }

            creator = CameraNodeCreator()
            product = creator.create(node["name"], node["ip"], node["department"])
            product.send_server_credentials(request.get_port(), "/Auth/api/credentials/camera_node/", request.auth)

        except (ObjectDoesNotExist, ObjectAlreadyExists) as e:
            raise NotAcceptable({"error": f"{e}"})

        except (ServerDown, ServerBadResponse) as e:
            product.delete_objects()
            raise NotAcceptable({"error": f"{e}"})

        except MultiValueDictKeyError as e:
            raise NotAcceptable({"error": f"Dato faltante: {e}"})

        return Response({"success": "Sensor creado"}, status=status.HTTP_201_CREATED)

    @staticmethod
    def list(request):
        node_data = CameraNode.objects.all().order_by("-id")
        serializer = CameraNodeSerializer(node_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def retrieve(request, camera_id):

        try:
            camera_node = CameraNode.objects.get(id=camera_id)
        except CameraNode.DoesNotExist as e:
            raise NotAcceptable({"error": f"El sensor no existe"})

        serializer = CameraNodeSerializer(camera_node, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def partial_update(request, camera_id):
        try:
            camera_node = CameraNode.objects.get(id=camera_id)
        except CameraNode.DoesNotExist as e:
            raise NotAcceptable({"error": f"El sensor no existe"})

        serializer = CameraNodeSerializer(instance=camera_node, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

        if not serializer.is_valid():
            raise NotAcceptable()

        instance = serializer.instance
        node_password = secrets.token_urlsafe(16)
        instance.user_node.set_password(node_password)

        try:
            send_server_credentials(instance.user_node.username, node_password, instance.user_node.ip,
                                    request.get_port())
        except ValueError as e:
            raise NotAcceptable(f"{e}")

        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def destroy(request, camera_id):
        try:
            camera_node = CameraNode.objects.get(id=camera_id)
        except CameraNode.DoesNotExist:
            raise NotAcceptable({"error": f"El sensor no existe"})

        camera_node.delete()

        return Response({"success": f"Sensor {camera_node.id} eliminado"}, status.HTTP_200_OK)
