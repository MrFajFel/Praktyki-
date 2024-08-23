import re

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Class, Computer, User
from app.serializers import UserSerializer


# Create your views here.
class API(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            hostname = serializer.validated_data.get('hostname')
            classroom = re.findall("[A-Z]\\d{2}", hostname.upper())
            classroom = classroom[0] if len(classroom) == 1 else None
            computer_name = re.findall("H\\w+$", hostname.upper())
            computer_name = computer_name[0][1:] if len(computer_name) == 1 else None
            classroom = Class.objects.get_or_create(name=classroom)
            computer = Computer.objects.get_or_create(name=computer_name, classroom=classroom[0])
            user = User.objects.create(first_name=serializer.validated_data.get('first_name'),
                                       last_name=serializer.validated_data.get('last_name'),
                                       computer=computer[0])
            user.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)