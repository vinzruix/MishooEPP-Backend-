import socket
import requests
from sensors.models import  SensorNode
from users.models import User


def ping_url(url):
    response = requests.get(url)

    if not response.ok:
        raise ValueError("The url cant be reach")

    return True


def send_server_credentials(id_device, password, esp_url):

    current_server_url = socket.gethostbyname(socket.gethostname())

    payload = {
        "id": id_device,
        "password": password,
        "server" : current_server_url
    }

    response = requests.post(f"{esp_url}/auth/", payload)
    
    if not response.ok:
        raise ValueError("The url server did not respond correctly")

    return True

    


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
    return node
