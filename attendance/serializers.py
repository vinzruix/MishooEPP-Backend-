from rest_framework import serializers

from attendance.models import WorkerArrival


class WorkerArrivalSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerArrival
        fields = ['id','worker','arrival_image','arrival_timestamp']