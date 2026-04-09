from rest_framework import serializers

from department.models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    permission = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ["id","name","epp","group","permission"]
        ordering = ["-id"]

    def get_permission(self,obj):
        return list(
            obj.group.permissions.values_list("codename", flat=True)
        )



class DepartmentSimpleSerializer(DepartmentSerializer):
    class Meta(DepartmentSerializer.Meta):
        fields = ["id","name"]
        ordering = ["-id"]
