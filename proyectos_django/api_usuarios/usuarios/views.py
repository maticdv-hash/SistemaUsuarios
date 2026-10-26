from rest_framework import viewsets
from .serializer import UsuarioSerializador, PermisoSerializador
from .models import Usuario, Permiso

class PermisoViewSet(viewsets.ModelViewSet):
    queryset = Permiso.objects.all()
    serializer_class = PermisoSerializador

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializador