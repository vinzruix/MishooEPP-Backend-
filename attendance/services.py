import requests


def deny_door_access():

    try:
        response = requests.get(f"http://192.168.0.105:80/door/denied/")

        if not response.ok:
            print("The door send an error message")

    except requests.exceptions.ConnectionError:
        print("Server down")




def allow_door_access():

    try:
        response = requests.get(f"http://192.168.0.105:80/door/allowed/")

        if not response.ok:
            print("The door send an error message")

    except requests.exceptions.ConnectionError:
        print("Server down")


