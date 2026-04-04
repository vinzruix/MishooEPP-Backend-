import socket
import requests
from django.contrib.auth.models import Permission

from sensors.models import  SensorNode
from users.models import User


def ping_url(url):
    response = requests.get(url)

    if not response.ok:
        raise ValueError("The url cant be reach")

    return True


def send_server_credentials(id_device, password, esp_url):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]

    payload = {
        "id": str(id_device),
        "password": password,
        "server" : ip
    }


    response = requests.post(f"{esp_url}/auth/", json=payload)
    
    if not response.ok:
        raise ValueError("The url server did not respond correctly")

    return response.status_code

    


def create_sensor_node(name,location,ip, user):

    if SensorNode.objects.filter(id=user.username):
        raise ValueError("There is a already a node with this id")
    
    new_node = SensorNode()
    new_node.id = user.username
    new_node.name = name
    new_node.location = location
    new_node.ip = ip
    new_node.user_node = user
    new_node.is_active = True
    new_node.save()

    return new_node

def create_user_node(username,password):
    
    if User.objects.filter(username=username):
        raise ValueError("There is a already a user_node with this username")


    node = User()
    node.username = username
    node.set_password(password)
    node.is_device = True
    node.save()

    node.user_permissions.add(Permission.objects.get(codename="view_all_user"))

    
    return node
