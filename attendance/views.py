from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from attendance.models import WorkerArrival
from attendance.serializers import WorkerArrivalSerializer


# Create your views here.


class AttendanceListAPIView(APIView):

    def get(self,request):
        attendances = WorkerArrival.objects.order_by("-arrival_timestamp")
        serializer = WorkerArrivalSerializer(attendances,many=True)
        return Response(serializer.data)

