from rest_framework import status
from rest_framework.exceptions import NotAcceptable
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from MishooEPP_Backend.permissions import permission_required
from incidence.models import Incidence
from incidence.serializers import IncidenceSerializer


# Create your views here.


class IncidenceViewSet(ViewSet):

    def get_permissions(self):
        if self.action == "create":
            return [permission_required('sensors.create_data_sensor')()]
        if self.action == "list":
            return [permission_required("sensors.view_all_sensor")()]
        if self.action == "retrieve":
            return [permission_required("sensors.view_all_sensor")()]

        return [IsAuthenticated()]


    @staticmethod
    def create(request):


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
            raise NotAcceptable()


        return Response({"success":"Incidencia creada"},status=status.HTTP_201_CREATED)



    @staticmethod
    def list(request):
        epp_sensor_data = Incidence.objects.order_by("-id")
        serializer = IncidenceSerializer(epp_sensor_data, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)



    @staticmethod
    def retrieve(request,epp_node_id):
        epp_sensor_data = Incidence.objects.filter(node_id=epp_node_id).order_by("-id")
        serializer = IncidenceSerializer(epp_sensor_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
