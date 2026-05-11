import secrets
import socket
import uuid
from abc import ABC, abstractmethod
import requests
from django.contrib.auth.models import Permission

from MishooEPP_Backend.core.models import Node
from MishooEPP_Backend.exeptions import ObjectDoesNotExist, ObjectAlreadyExists, ServerDown, ServerBadResponse
from department.models import Department
from epp_detection.models import EPPNode
from face_detection.models import CameraNode
from sensors.models import SensorNode
from users.models import User


class Creator(ABC):

    @staticmethod
    def _create_user_node(username):
        if User.objects.filter(username=username).exists():
            raise ObjectDoesNotExist("Ya hay un nodo con este nombre")

        node = User.objects.create_user(
            is_active=True,
            username=username,
            is_device=True,
        )

        node.user_permissions.add(Permission.objects.get(codename="create_data_sensor"))

        return node

    def create(self, name, ip,department):
        node_user = self._create_user_node(username=uuid.uuid4())
        product = self.factory_method(node_user=node_user)
        product.generate_node(name,ip,department)
        product.set_user_password()

        return product

    @abstractmethod
    def factory_method(self, node_user):
        pass


class SensorNodeCreator(Creator):

    def factory_method(self, node_user):
        return SensorNodeProduct(node_user)


class EPPNodeCreator(Creator):

    def factory_method(self, node_user):
        return EPPNodeProduct(node_user)


class CameraNodeCreator(Creator):

    def factory_method(self, node_user):
        return CameraNodeProduct(node_user)




class Product(ABC):

    def __init__(self, user_node: User):
        self.node_password = ""
        self.user_node = user_node
        self.sensor_node = None
        self.node_url = ""

    @staticmethod
    def _create_node(sensor_cls: Node, user: User, name, ip, department):

        if sensor_cls.objects.filter(id=user.username).exists():
            raise ObjectAlreadyExists("Ya hay un nodo con este nombre")

        if not Department.objects.filter(name=department).exists():
            raise ObjectAlreadyExists("No existe este departamento")

        new_node = sensor_cls.objects.create(
            id=user.username,
            name=name,
            ip=ip,
            department=Department.objects.get(name=department),
            user_node=user,
            is_active=True,

        )

        return new_node

    def send_server_credentials(self, port, node_url, token):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]

        try:
            response = requests.post(
                f"{self.sensor_node.ip}{node_url}",
                json={
                    "id": str(self.user_node.username),
                    "password": self.node_password,
                    "server": f"{ip}:{port}"
                },
                headers={
                    "Authorization": f"Bearer {token}"
                })

            if not response.ok:
                raise ServerBadResponse("El nodo destino no respondio correctamente")


        except (requests.exceptions.ConnectionError, requests.exceptions.MissingSchema):
            raise ServerDown("El nodo destino parace estar caido")

    def set_user_password(self):
        if self.user_node:
            self.node_password = secrets.token_urlsafe(16)
            self.user_node.set_password(self.node_password)
            self.user_node.save()

    def delete_objects(self):

        if self.user_node:
            self.user_node.delete()
        if self.sensor_node:
            self.sensor_node.delete()

    @abstractmethod
    def generate_node(self, name, ip,department):
        pass


class SensorNodeProduct(Product):

    def generate_node(self, name, ip,department):
        self.sensor_node = self._create_node(SensorNode, self.user_node, name, ip,department)


class EPPNodeProduct(Product):

    def generate_node(self, name,ip, department):
        self.sensor_node = self._create_node(EPPNode, self.user_node, name, ip,department)


class CameraNodeProduct(Product):

    def generate_node(self, name, ip,department):
        self.sensor_node = self._create_node(CameraNode, self.user_node, name, ip,department)

