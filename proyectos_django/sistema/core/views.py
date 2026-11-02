from django.shortcuts import render, redirect
import requests

API_URL = "http://127.0.0.1:8050/api/autentificar/"

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            response = requests.post(API_URL, json={
                'username': username,
                'password': password
            })

            if response.status_code == 200:
                data = response.json()
                request.session['usuario'] = data.get('usuario')
                request.session['permisos'] = data.get('permisos', [])
                return redirect('menu')
            else:
                error = "Usuario o contraseña incorrectos."
        except requests.exceptions.ConnectionError:
            error = "No se pudo conectar con la API (puerto 8050 apagado)."

    return render(request, 'core/login.html', {'error': error})

def menu_view(request):
    usuario = request.session.get('usuario')
    permisos = request.session.get('permisos', [])

    if not usuario:
        return redirect('login')

    return render(request, 'core/menu.html', {
        'usuario': usuario,
        'permisos': permisos
    })

def logout_view(request):
    request.session.flush()
    return redirect('login')