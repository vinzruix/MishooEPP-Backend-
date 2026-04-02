import uuid
from symtable import Class

from django.db import models

from MishooEPP_Backend.core.models import Node
from users.models import User


# Create your models here.


class SensorNode(Node):
    user_node = models.OneToOneField(User, related_name="sensor_nodes", on_delete=models.CASCADE, null=True)


class Temperature(models.Model):
    class Meta:
        permissions = [
            ("view_all_sensor", "Can view all the sensors")
        ]

    date = models.DateTimeField(auto_now=True)
    value = models.DecimalField(decimal_places=2, max_digits=6)

class Humidity(models.Model):
    date = models.DateTimeField(auto_now=True)
    value = models.DecimalField(decimal_places=2, max_digits=6)

class Pressure(models.Model):
    date = models.DateTimeField(auto_now=True)
    value = models.DecimalField(decimal_places=2, max_digits=6)

class CO2(models.Model):
    date = models.DateTimeField(auto_now=True)
    value = models.DecimalField(decimal_places=2, max_digits=6)

class TVOC(models.Model):
    date = models.DateTimeField(auto_now=True)
    value = models.DecimalField(decimal_places=2, max_digits=6)


