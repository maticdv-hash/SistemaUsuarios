from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import UsuarioSerializador, PermisoSerializador
from .models import Usuario, Permiso

class PermisoViewSet(viewsets.ModelViewSet):
    queryset = Permiso.objects.all()
    serializer_class = PermisoSerializador

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializador

# Nuevo endpoint requerido por la evaluación
class AutentificarView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        try:
            # Busca al usuario con esas credenciales exactas
            usuario = Usuario.objects.get(username=username, password=password)
            
            if not usuario.is_active:
                return Response({'error': 'Usuario inactivo'}, status=status.HTTP_401_UNAUTHORIZED)
            
            # Obtiene los permisos asociados al usuario
            permisos_usuario = usuario.permisos.all()
            lista_permisos = [permiso.codigo for permiso in permisos_usuario]
            
            # Retorna el JSON con los servicios/permisos
            return Response({
                'mensaje': 'Autenticación exitosa',
                'usuario': usuario.username,
                'permisos': lista_permisos
            }, status=status.HTTP_200_OK)
            
        except Usuario.DoesNotExist:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)