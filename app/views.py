import re

from django.shortcuts import render, get_object_or_404, redirect
from app.form import LogForm
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponseRedirect
from django.urls import reverse
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
#
# class Info(ListView):
#     queryset = User.objects.all()
#     context_object_name = 'infos'
#     paginate_by = 9
#     template_name = 'logs.html'
#     def sprawdzenie(request):
#         if request.COOKIES.get('Zalogowany') != '1':
#             return redirect('app:logowanie')
class Info(ListView):
    queryset = User.objects.all()
    context_object_name = 'infos'
    paginate_by = 9
    template_name = 'logs.html'

    def get(self, request, *args, **kwargs):
        # Sprawdzenie, czy ciasteczko 'Zalogowany' ma wartość '1'
        if request.COOKIES.get('Zalogowany') != '1':
            # Jeśli ciasteczko nie istnieje lub ma inną wartość, przekierowanie na stronę logowania
            return redirect('app:logowanie')

        # Jeśli ciasteczko jest poprawne, kontynuuj z renderowaniem widoku
        return super().get(request, *args, **kwargs)




def info_detail(request,year,month,day):
    info = get_object_or_404(User,
                                last_reported__year = year,
                                last_reported__month = month,
                                last_reported__day = day,
                                )
    return render(request,"logs.html" ,{'infos': infos})


def logowanie(request):
    if request.method == 'POST':
        form = LogForm(request.POST)
        if form.is_valid():
            # Sprawdzenie danych logowania
            for user in User.objects.all():
                if (
                        form.cleaned_data['first_name'] == user.first_name and
                        form.cleaned_data['last_name'] == user.last_name and
                        form.cleaned_data['computer'] == user.computer
                ):
                    # Tworzenie odpowiedzi z przekierowaniem
                    response = HttpResponseRedirect('/logs/')  # lub reverse('app:info')
                    response.set_cookie("Zalogowany", '1')  # Ustawienie ciasteczka
                    return response

            # Jeśli dane logowania są niepoprawne, przekaż błąd
            form.add_error(None, "Niepoprawne dane logowania")

    else:
        form = LogForm()

    return render(request, 'logowanie.html', {'form': form})

def wyloguj(request):
    # Tworzenie obiektu odpowiedzi
    response = HttpResponseRedirect('/logs/')

    # Usuwanie ciasteczka o nazwie 'Zalogowany'
    response.delete_cookie('Zalogowany')

    return response


def delete_info(request, year, month, day):
    info = get_object_or_404(User,
                             last_reported__year=year,
                             last_reported__month=month,
                             last_reported__day=day,
                             )
    info.delete()
    return redirect('/logs')