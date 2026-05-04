from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import NotAcceptable, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from MishooEPP_Backend.core.instances import face_recognition
from MishooEPP_Backend.permissions import permission_required
from face_detection.exeptions import NumFaceError, NoFacesData, UserNotRegistered
from face_detection.services import MediaConverter
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


        incidence = {
            "image" : request.FILES['image'],
            "missing_epp" : request.data.getlist('missing_epp'),
            "user_node" : request.user.id,
            "node" : request.user.epp_nodes.id,
        }


        serializer = IncidenceSerializer(data=incidence)

        if serializer.is_valid():
            serializer.save()


        if not serializer.is_valid():
            print(serializer.errors)
            raise NotAcceptable()



        return Response({"success":"Incidence created"},status=status.HTTP_201_CREATED)




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
