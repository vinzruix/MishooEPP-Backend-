from rest_framework import serializers

from department.models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ["id","name","epp","group","permissions"]
        ordering = ["-id"]

    def get_permissions(self,obj):
        return list(
            obj.group.permissions.values_list("codename", flat=True)
        )



class DepartmentSimpleSerializer(DepartmentSerializer):
    class Meta(DepartmentSerializer.Meta):
        fields = ["id","name"]
        ordering = ["-id"]
