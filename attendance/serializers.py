from rest_framework import serializers

from attendance.models import WorkerArrival
from users.serializers import UserSerializer


class WorkerArrivalSerializer(serializers.ModelSerializer):
    worker = UserSerializer(read_only=True)

    class Meta:
        model = WorkerArrival
        fields = ['id','worker','arrival_image','node','arrival_timestamp']
