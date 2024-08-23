from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    hostname = serializers.CharField(max_length=100)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)


