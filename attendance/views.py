from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from MishooEPP_Backend.permissions import permission_required
from attendance.models import WorkerArrival
from attendance.serializers import WorkerArrivalSerializer


# Create your views here.


class AttendanceListAPIView(APIView):

    permission_classes = [permission_required("attendance.view_all_workerarrival")]

    def get(self,request):
        attendances = WorkerArrival.objects.order_by("-arrival_timestamp")
        serializer = WorkerArrivalSerializer(attendances,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAttendanceDetailAPIView(APIView):
    def get(self,request,pk):

        user_attendance = WorkerArrival.objects.filter(worker_id=pk).order_by("-arrival_timestamp")

        if not user_attendance:
            raise NotFound({"error":f"User id {pk} not found"})


        serializer = WorkerArrivalSerializer(user_attendance, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
