from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from MishooEPP_Backend.permissions import permission_required
from incidence.models import Incidence
from incidence.serializers import IncidenceSerializer


# Create your views here.



class IncidenceCreateListApiView(APIView):

    def get_permissions(self):
        if self.request.method == "POST":
            return [permission_required('sensors.create_data_sensor')()]
        if self.request.method == "GET":
            return [permission_required("sensors.view_all_sensor")()]

        return [IsAuthenticated()]


    @staticmethod
    def post(request):


        image = request.FILES['image']
        datetime = request.data['datetime']
        missing_epp = request.data['missing_epp']
        user = request.user



    @staticmethod
    def get(request):
        epp_sensor_data = Incidence.objects.order_by("-id")
        serializer = IncidenceSerializer(epp_sensor_data, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class IncidenceDetailPatchDelete(APIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return [permission_required('sensors.view_all_sensor')()]

        return [IsAuthenticated()]

    @staticmethod
    def get(request,epp_node_id):
        epp_sensor_data = Incidence.objects.filter(node_id=epp_node_id)
        serializer = IncidenceSerializer(epp_sensor_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
