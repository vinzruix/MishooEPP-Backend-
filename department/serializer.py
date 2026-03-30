from rest_framework import serializers

from department.models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id","name","epp","group"]

class DepartmentSimpleSerializer(DepartmentSerializer):
    class Meta(DepartmentSerializer.Meta):
        fields = ["id","name"]
