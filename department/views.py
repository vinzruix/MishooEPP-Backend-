import json

from django.contrib.auth.models import Group
from django.db import transaction
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import NotAcceptable
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from sympy import true

from MishooEPP_Backend.permissions import permission_required
from department.models import Department
from department.serializer import DepartmentSerializer, DepartmentSimpleSerializer
from department.services import create_group, create_department, get_department


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
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        department = {
            "name": request.data["name"],
            "epp": json.loads(request.data["epp"]),
            "permissions": request.data.getlist("permissions")
        }

        try:
            with transaction.atomic():
                new_group = create_group(department["name"], department["permissions"])
                new_department = create_department(new_group, department["epp"])
        except ValueError as e:
            raise NotAcceptable({"error": f"{e}"})

        return Response({"success": f"department {new_department.name} created"}, status=status.HTTP_201_CREATED)


class DepartmentDetailApiView(APIView):

    def patch(self,request,department_id):
        try:
            department = get_department(department_id)
        except Exception as e:
            raise NotAcceptable({"error":f"{e}"})

        serializer = DepartmentSerializer(department,request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"success":f"Departamento actualizado"})


        raise NotAcceptable({"error":f"data not valid"})

    def delete(self,request,department_id):
        try:
            department = get_department(department_id)
        except Exception as e:
            raise NotAcceptable({"error":f"{e}"})

        department.delete()

        return Response({"success":"department eliminated"})









class DepartmentListSimpleApiView(APIView):

    permission_classes = [permission_required("users.create_user") | permission_required("department.view_all_department")]

    def get(self,request):
        departments = Department.objects.all()
        serializer = DepartmentSimpleSerializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
