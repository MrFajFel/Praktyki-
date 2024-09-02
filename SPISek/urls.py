
from django.contrib import admin
from django.urls import path,include

from app.views import API

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', API.as_view()),
path('', include('app.urls', namespace='Informacje.O.Uzytkowniku')),
]
