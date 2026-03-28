from django.contrib.auth.models import Group
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from sympy import true

from department.models import Department
from department.serializer import DepartmentSerializer
from department.services import create_group


# Create your views here.


class DepartmentListApiView(APIView):


    def get(self,request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)


    def post(self,request):

        department = {
            "name" : request.data["name"],
            "epp" : request.data["epp"],
            "permissions" : request.data["permissions"]
        }

        new_group = create_group(department["name"], department["permissions"])
        new_group.save()

        new_department = Department()
        new_department.name = department["name"]
        new_department.group = new_group
        new_department.epp = department["epp"]
        new_department.save()

        return Response({"success":f"department {new_department.name} created"})




