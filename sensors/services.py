import socket
import requests
from django.contrib.auth.models import Permission
from django.db import transaction

from department.models import Department
from sensors.models import SensorNode, Temperature, Humidity, CO2, TVOC
from users.models import User


def ping_url(url):
    response = requests.get(url)

    if not response.ok:
        raise ValueError("The url cant be reach")

    return True


def send_server_credentials(id_device, password, esp_url,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]

    payload = {
        "id": str(id_device),
        "password": password,
        "server" : f"{ip}:{port}"
    }

    response = requests.post(f"{esp_url}/Auth/api/credentials/", json=payload)
    
    if not response.ok:
        raise ValueError("The url server did not respond correctly")

    return response.status_code

    


def create_sensor_node(name,ip, user):

    if SensorNode.objects.filter(id=user.username):
        raise ValueError("There is a already a node with this id")
    
    new_node = SensorNode()
    new_node.id = user.username
    new_node.name = name
    new_node.ip = ip
    new_node.user_node = user
    new_node.is_active = True
    new_node.save()

    return new_node

def create_user_node(username,password):
    
    if User.objects.filter(username=username):
        raise ValueError("There is a already a user_node with this username")


    node = User()
    node.is_active = True
    node.username = username
    node.set_password(password)
    node.is_device = True
    node.save()

    node.user_permissions.add(Permission.objects.get(codename="create_data_sensor"))

    
    return node

def get_sensor_node(sensor_id):
    try:
        return SensorNode.objects.get(id=sensor_id)
    except SensorNode.DoesNotExist:
        raise ValueError("Node not found")


def create_all_sensor_data(user,tem,hum,co2,tvoc):
    try:
        with transaction.atomic():

            Temperature.objects.create(value=tem, node=user.sensor_nodes)
            Humidity.objects.create(value=hum, node=user.sensor_nodes)
            CO2.objects.create(value=co2, node=user.sensor_nodes)
            TVOC.objects.create(value=tvoc, node=user.sensor_nodes)

    except Exception as e:
        raise ValueError(f"{e}")
