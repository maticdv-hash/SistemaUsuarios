from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'usuarios', views.UsuarioViewSet)
router.register(r'permisos', views.PermisoViewSet)

urlpatterns = [
    path('', include(router.urls))
]