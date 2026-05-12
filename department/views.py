import json
from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import NotAcceptable
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from MishooEPP_Backend.permissions import permission_required
from department.models import Department
from department.serializer import DepartmentSerializer, DepartmentSimpleSerializer
from department.services import create_group, create_department, get_department, add_permissions


# Create your views here.


class DepartmentViewSet(ViewSet):

    def get_permissions(self):

        if self.action == "list":
            return [permission_required('department.view_all_department')()]
        if self.action == "create":
            return [permission_required("department.create_department")()]
        if self.action == "partial_update":
            return [permission_required("department.create_department")()]
        if self.action == "destroy":
            return [permission_required("department.create_department")()]


        return [IsAuthenticated()]

    @staticmethod
    def list(request):

        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def create(request):

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

        return Response({"success": f"Departamento {new_department.name} creado"}, status=status.HTTP_201_CREATED)

    @staticmethod
    def partial_update(request,department_id):
        try:
            department = get_department(department_id)
        except Exception as e:
            raise NotAcceptable({"error":f"{e}"})

        serializer = DepartmentSerializer(department,request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            serializer.instance.group.permissions.clear()
            add_permissions(serializer.instance.group, request.data["permissions"])

        if not serializer.is_valid():
            raise NotAcceptable({"error": f"data not valid"})

        return Response({"success":f"Departamento actualizado"})



    @staticmethod
    def destroy(request,department_id):
        try:
            department = get_department(department_id)
        except Exception as e:
            raise NotAcceptable({"error":f"{e}"})

        department.delete()

        return Response({"success":"department eliminated"})






class DepartmentSimpleViewSet(ViewSet):

    def get_permissions(self):
        if self.action == "list":
            return [permission_required("department.view_all_department")()]
        return [IsAuthenticated()]

    @staticmethod
    def list(request):
        departments = Department.objects.all()
        serializer = DepartmentSimpleSerializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
