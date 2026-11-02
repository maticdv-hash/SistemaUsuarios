from django.urls import path
from . import views

urlpatterns = [
    # Autenticación de usuarios
    path('autentificar/', views.autentificar, name='autentificar'),
    
    # Gestión de usuarios
    path('agregarusuario/', views.agregar_usuario, name='agregar_usuario'),
    path('agregarusuario', views.agregar_usuario),  # Alternativa sin slash por compatibilidad
    path('actualizar/', views.actualizar_usuario, name='actualizar_usuario'),
    
    # Gestión de permisos
    path('addpermiso/', views.agregar_permiso, name='agregar_permiso'),
    path('asociapermiso/', views.asociar_permiso, name='asociar_permiso'),
]