from rest_framework_json_api import serializers
from authorized.models import Applications

class AuthorizedAppSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    can_request = serializers.BooleanField(default=True)

    class Meta:
        model = Applications
        fields = ('name', 'can_request')
