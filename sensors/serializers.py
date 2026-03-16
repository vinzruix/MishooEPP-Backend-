from rest_framework import serializers
from sensors.models import Temperature, Humidity, Pressure, CO2, TVOC


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


