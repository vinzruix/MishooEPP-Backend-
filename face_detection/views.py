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
from face_detection.models import CameraNode
from face_detection.serializers import CameraNodeObtainPairSerializer, CameraNodeSerializer
from face_detection.services import create_camera_node, send_server_credentials, get_camera_node
from sensors.services import create_user_node


class CameraNodeObtainPairSerializerAPIView(TokenObtainPairView):
    serializer_class = CameraNodeObtainPairSerializer


class CameraNodeCreateAPIView(APIView):

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

        try:
            with transaction.atomic():
                node_username = uuid.uuid4()
                node_password = secrets.token_urlsafe(16)

                node_user = create_user_node(node_username, node_password)

                create_camera_node(node["name"], node["department"], node["ip"], node_user)

                transaction.on_commit(
                    lambda: send_server_credentials(node_username, node_password, node["ip"], request.get_port())
                )

        except ValueError as e:
            raise NotAcceptable({"error": f"{e}"})

        return Response({"success": f"Sensor creado"}, status=status.HTTP_201_CREATED)

    @staticmethod
    def get(request):
        node_data = CameraNode.objects.all().order_by("-id")
        serializer = CameraNodeSerializer(node_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CameraNodeDetailPatchDeleteAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [permission_required("sensors.view_all_sensor")()]

        if self.request.method == "patch":
            return [permission_required("sensors.create_sensor")()]

        if self.request.method == "delete":
            return [permission_required("sensors.create_sensor")()]
        return [IsAuthenticated()]

    @staticmethod
    def get(request, camera_id):

        try:
            node_data = get_camera_node(camera_id)
        except Exception as e:
            raise NotAcceptable({"error": f"{e}"})

        serializer = CameraNodeSerializer(node_data, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def patch(request, camera_id):
        try:
            node_data = get_camera_node(camera_id)
        except Exception as e:
            raise NotAcceptable({"error": f"{e}"})

        serializer = CameraNodeSerializer(instance=node_data, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        raise NotAcceptable({"error": "error"})

    @staticmethod
    def delete(request, camera_id):
        try:
            sensor_node = get_camera_node(camera_id)
        except Exception as e:
            raise NotAcceptable({"error": f"{e}"})

        sensor_node.delete()

        return Response({"success": f"{camera_id.id} eliminated"}, status.HTTP_200_OK)
