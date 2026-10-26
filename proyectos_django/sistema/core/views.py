from django.shortcuts import render
import requests

def verificar_acceso(request):
    try:
        # Petición GET a tu API en el puerto 8050
        respuesta = requests.get('http://127.0.0.1:8050/api/usuarios/')
        usuarios = respuesta.json() if respuesta.status_code == 200 else []
    except requests.exceptions.ConnectionError:
        usuarios = [] 

    return render(request, 'core/menu.html', {'usuarios': usuarios})