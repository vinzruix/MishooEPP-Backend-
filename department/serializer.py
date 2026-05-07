from rest_framework import serializers

from department.models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    permission = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ["id","name","epp","group","permission"]
        ordering = ["-id"]





class DepartmentSimpleSerializer(DepartmentSerializer):
    class Meta(DepartmentSerializer.Meta):
        fields = ["id","name"]
        ordering = ["-id"]
