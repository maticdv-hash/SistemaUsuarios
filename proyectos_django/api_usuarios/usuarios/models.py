from django.db import models

class Permiso(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50, unique=True, help_text="Ejemplo: VER_REPORTES, ADMIN_USUARIOS")

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    # Relación muchos a muchos: Un usuario puede tener varios permisos
    permisos = models.ManyToManyField(Permiso, blank=True)

    def __str__(self):
        return self.username
