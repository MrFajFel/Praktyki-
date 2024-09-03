import re

from django.shortcuts import render, get_object_or_404, redirect
from app.form import LogForm
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import HttpResponse
from app.models import Class, Computer, User
from app.serializers import UserSerializer
from django.views.generic import ListView

from django.shortcuts import render, get_object_or_404

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
class Info(ListView):
    queryset = User.objects.all()
    context_object_name = 'infos'
    paginate_by = 9
    template_name = 'logs.html'

def info_detail(request,year,month,day):
    info = get_object_or_404(User,
                                last_reported__year = year,
                                last_reported__month = month,
                                last_reported__day = day,)
    return render(request,"logs.html" ,{'infos': infos})

def logowanie(request):
    if request.method == 'POST':
        form = LogForm(request.POST)
        if form.is_valid():
            # if User.objects.all().filter(username=form.cleaned_data['']).exists():
                return redirect('app:info')
        else:
            form = LogForm()
    else:
        form = LogForm()
    return render(request, 'logowanie.html', {'form': form})
