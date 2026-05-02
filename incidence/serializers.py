from rest_framework import serializers

from incidence.models import Incidence


class IncidenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Incidence
        fields = ["id","image","missing_epp","user_node","datetime",'node']
