from typing import Any
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import AuthUser, TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

from sensors.models import Temperature, Humidity, Pressure, CO2, TVOC, SensorNode


class SensorNodeObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs: dict[str, Any]) -> dict[Any, Any]:
        try:
            data = super().validate(attrs)
        except Exception:
            raise AuthenticationFailed({"error":"invalid credentials"})

        

        if not SensorNode.objects.filter(user_node=self.user).exists():
            raise AuthenticationFailed({"error":"invalid credentials"})
        
        node = SensorNode.objects.get(user_node=self.user)

        if not node.is_active:
            raise AuthenticationFailed({"error":"device not active"})

        return data


    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        token = super().get_token(user)
        token['is_device'] = True
        token['id_node'] = user.username
        return token



class EnvironmentSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorNode
        fields = ["name", "location", "is_active", ]


class SensorBaseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["date","value"]

    def to_representation(self, instance):
        new_date = super().to_representation(instance)
        new_date["date"] = instance.date.strftime("%H:%M:%S")
        return new_date



class TemperatureSerializer(SensorBaseSerializer):
    class Meta(SensorBaseSerializer.Meta):
        model = Temperature


class HumiditySerializer(SensorBaseSerializer):
    class Meta(SensorBaseSerializer.Meta):
        model = Humidity


class PressureSerializer(SensorBaseSerializer):
    class Meta(SensorBaseSerializer.Meta):
        model = Pressure


class CO2Serializer(SensorBaseSerializer):
    class Meta(SensorBaseSerializer.Meta):
        model = CO2

class TVOCSerializer(SensorBaseSerializer):
    class Meta(SensorBaseSerializer.Meta):
        model = TVOC


