from django.contrib.auth.models import Group
from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import NotAcceptable
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from sympy import true

from MishooEPP_Backend.permissions import permission_required
from department.models import Department
from department.serializer import DepartmentSerializer, DepartmentSimpleSerializer
from department.services import create_group, create_department


# Create your views here.


class DepartmentListApiView(APIView):

    def get_permissions(self):

        if self.request.method == "GET":
            return [permission_required('department.view_all_department')()]
        if self.request.method == "POST":
            return [permission_required("department.create_department")()]

        return [IsAuthenticated()]

    def get(self,request):

        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)


    def post(self,request):

        department = {
            "name" : request.data["name"],
            "epp" : request.data.getlist("epp"),
            "permissions" : request.data.getlist("permissions")
        }

        try:
            new_group = create_group(department["name"], department["permissions"])
            new_department = create_department(new_group, department["epp"])
        except ValueError as e:
            raise NotAcceptable({"error": f"{e}"})

                                                               
        return Response({"success":f"department {new_department.name} created"})



class DepartmentListSimpleApiView(APIView):

    permission_classes = [permission_required("users.create_user") | permission_required("department.view_all_department")]

    def get(self,request):
        departments = Department.objects.all()
        serializer = DepartmentSimpleSerializer(departments, many=True)
        return Response(serializer.data)
