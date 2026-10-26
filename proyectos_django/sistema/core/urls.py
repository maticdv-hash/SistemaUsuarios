from django.urls import path
from . import views

urlpatterns = [
    path('', views.verificar_acceso, name='menu'),
]