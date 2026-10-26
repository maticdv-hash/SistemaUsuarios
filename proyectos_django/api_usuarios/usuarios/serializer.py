from rest_framework import serializers
from .models import Usuario, Permiso

class PermisoSerializador(serializers.ModelSerializer):
    class Meta:
        model = Permiso
        fields = '__all__'

class UsuarioSerializador(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'