import socket

import requests

from department.models import Department
from epp_detection.models import EPPNode


def create_epp_node(name, department, ip, user):
    if EPPNode.objects.filter(id=user.username):
        raise ValueError("There is a already a node with this id")

    new_node = EPPNode()
    new_node.id = user.username
    new_node.name = name
    new_node.department = Department.objects.get(name=department)
    new_node.ip = ip
    new_node.user_node = user
    new_node.is_active = True
    new_node.save()

    return new_node


def send_server_credentials(id_device, password, esp_url, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]

    payload = {
        "id": str(id_device),
        "password": password,
        "server": f"{ip}:{port}"
    }

    response = requests.post(f"{esp_url}/Auth/api/credentials/epp_node/", json=payload)

    if not response.ok:
        raise ValueError("The url server did not respond correctly")

    return response.status_code


def get_epp_node(epp_id):
    try:
        return EPPNode.objects.get(id=epp_id)
    except EPPNode.DoesNotExist:
        raise ValueError("Node not found")
