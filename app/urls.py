from django.urls import path

import app.views
from app import views

app_name = 'app'
urlpatterns = [
    path('tak/',views.Info.as_view() ,name='info')
]