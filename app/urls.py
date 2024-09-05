from django.urls import path

import app.views
from app import views

app_name = 'app'
urlpatterns = [
    path('logs/',views.Info.as_view() ,name='info'),
    path('',views.logowanie, name="logowanie"),
    path('wylogowanie/', views.wyloguj, name="wylogowanie"),
    path('logs/delete/<int:year>/<int:month>/<int:day>/', views.delete_info, name='delete_info'),
]