
from rest_framework import serializers

from attendance.models import WorkerArrival
from users.models import User
from users.serializers import UserSerializer


class WorkerArrivalSerializer(serializers.ModelSerializer):



    class Meta:
        model = WorkerArrival
        fields = ['id', 'worker', 'arrival_image', 'node', 'arrival_timestamp', 'user_node']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["worker"] = UserSerializer(instance.worker).data
        return rep