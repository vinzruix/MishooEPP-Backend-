import uuid
from symtable import Class

from django.db import models

from MishooEPP_Backend.core.models import Node
from users.models import User


# Create your models here.


class SensorNode(Node):
    class Meta:
        permissions = [
            ("create_sensor","Can create a new Sensor node")
        ]

    user_node = models.OneToOneField(User, related_name="sensor_nodes", on_delete=models.CASCADE, null=True)


class BaseDataSensor(models.Model):
    class Meta:
        abstract = True

    date = models.DateTimeField(auto_now=True)
    value = models.DecimalField(decimal_places=2, max_digits=6)


class Temperature(BaseDataSensor):
    class Meta:
        permissions = [
            ("view_all_sensor", "Can view all the sensors")
        ]

    node = models.ForeignKey(SensorNode, related_name="temperature_data", on_delete=models.CASCADE, null=True)



class Humidity(BaseDataSensor):
    node = models.ForeignKey(SensorNode, related_name="humidity_data", on_delete=models.CASCADE,null=True)


class Pressure(BaseDataSensor):
    node = models.ForeignKey(SensorNode, related_name="pressure_data", on_delete=models.CASCADE,null=True)


class CO2(BaseDataSensor):
    node = models.ForeignKey(SensorNode, related_name="co2_data", on_delete=models.CASCADE,null=True)


class TVOC(BaseDataSensor):
    node = models.ForeignKey(SensorNode, related_name="tvoc_data", on_delete=models.CASCADE,null=True)

