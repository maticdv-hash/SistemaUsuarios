from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate
from django.contrib.contenttypes.models import ContentType


@api_view(['POST'])
def autentificar(request):
    """
    Valida credenciales de usuario y retorna sus permisos asociados.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        # Obtener los códigos (codename) de todos los permisos asignados al usuario
        permisos = list(user.user_permissions.values_list('codename', flat=True))
        return Response({
            "valido": True,
            "usuario": user.username,
            "permisos": permisos
        }, status=status.HTTP_200_OK)
    
    return Response({
        "valido": False,
        "error": "Credenciales inválidas"
    }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
def agregar_usuario(request):
    """
    GET: Retorna el registro de todos los usuarios creados en la base de datos.
    POST: Crea un nuevo usuario en la API.
    """
    if request.method == 'GET':
        # Consulta los usuarios guardados en la BD
        usuarios = User.objects.all().values('id', 'username', 'email', 'date_joined')
        return Response({
            "total_usuarios": usuarios.count(),
            "registro_usuarios": list(usuarios)
        }, status=status.HTTP_200_OK)

    # Lógica POST para guardar un usuario
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')

    if not username or not password:
        return Response({
            "error": "Faltan datos obligatorios (username, password)"
        }, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({
            "error": "El nombre de usuario ya existe"
        }, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, email=email)
    return Response({
        "mensaje": "Usuario creado exitosamente",
        "id": user.id,
        "username": user.username
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def actualizar_usuario(request):
    """
    Actualiza la contraseña o email de un usuario existente.
    """
    username = request.data.get('username')
    new_password = request.data.get('new_password')
    new_email = request.data.get('new_email')

    try:
        user = User.objects.get(username=username)
        if new_password:
            user.set_password(new_password)
        if new_email:
            user.email = new_email
        user.save()
        return Response({"mensaje": "Usuario actualizado correctamente"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def agregar_permiso(request):
    """
    Crea un permiso personalizado en el sistema.
    """
    if request.method == 'GET':
        return Response({
            "mensaje": "Envíe 'codename' y 'name' mediante POST para registrar un permiso.",
            "permisos_disponibles_plantilla": ["VER_MENU", "ADMIN_USUARIOS", "VER_REPORTES"]
        }, status=status.HTTP_200_OK)

    codename = request.data.get('codename')
    name = request.data.get('name')

    if not codename or not name:
        return Response({"error": "Faltan parámetros 'codename' y 'name'"}, status=status.HTTP_400_BAD_REQUEST)

    content_type = ContentType.objects.get_for_model(User)
    
    permiso, created = Permission.objects.get_or_create(
        codename=codename,
        name=name,
        content_type=content_type
    )

    if created:
        return Response({"mensaje": "Permiso creado con éxito"}, status=status.HTTP_201_CREATED)
    return Response({"mensaje": "El permiso ya existía"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def asociar_permiso(request):
    """
    Asigna un permiso específico a un usuario.
    """
    username = request.data.get('username')
    codename = request.data.get('codename')

    try:
        user = User.objects.get(username=username)
        permiso = Permission.objects.get(codename=codename)
        user.user_permissions.add(permiso)
        return Response({"mensaje": f"Permiso '{codename}' asignado a '{username}' con éxito"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    except Permission.DoesNotExist:
        return Response({"error": "Permiso no encontrado"}, status=status.HTTP_404_NOT_FOUND)