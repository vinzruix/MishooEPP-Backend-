from rest_framework import status
from rest_framework.exceptions import NotFound, NotAcceptable
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from MishooEPP_Backend.core.instances import face_recognition
from MishooEPP_Backend.permissions import permission_required
from attendance.models import WorkerArrival
from attendance.serializers import WorkerArrivalSerializer
from face_detection.exeptions import UserNotRegistered, NumFaceError, NoFacesData



class AttendanceViewSet(ViewSet):

    def get_permissions(self):
        if self.request.method == "create":
            return [permission_required('sensors.create_data_sensor')()]
        if self.request.method == "list":
            return [permission_required("attendance.view_all_workerarrival")()]

        return [IsAuthenticated()]

    @staticmethod
    def create(request):

        try:
            worker, image = face_recognition.get_user_id_by_image(request.body)
        except (NumFaceError, NoFacesData) as e:
            raise NotAcceptable({"error": f"{e}"})
        except UserNotRegistered as e:
            raise NotFound({"error": f"{e}"})



        arrival = {
            "arrival_image": image,
            "worker": worker.id,
            "user_node": request.user.id,
            "node": request.user.camera_nodes.id,
        }

        serializer = WorkerArrivalSerializer(data=arrival)

        if not serializer.is_valid():
            raise NotAcceptable()

        if serializer.is_valid():
            serializer.save()

        return Response({"success": f"Usuario identificado como {worker.first_name}"}, status=status.HTTP_201_CREATED)

    @staticmethod
    def list(request):
        attendances = WorkerArrival.objects.order_by("-arrival_timestamp")
        serializer = WorkerArrivalSerializer(attendances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAttendanceViewSet(ViewSet):

    @staticmethod
    def retrieve(request, pk):
        user_attendance = WorkerArrival.objects.filter(worker_id=pk).order_by("-arrival_timestamp")
        serializer = WorkerArrivalSerializer(user_attendance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NodeAttendanceViewSet(ViewSet):

    @staticmethod
    def retrieve(request, pk):
        node_attendance = WorkerArrival.objects.filter(node_id=pk).order_by("-arrival_timestamp")
        serializer = WorkerArrivalSerializer(node_attendance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
