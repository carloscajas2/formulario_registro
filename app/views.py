from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import Agencia, Registro
import csv
from io import StringIO

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('manage')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login.html')

def manage_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_region_mapping = {
        'centro': 'CENTRO',
        'occidente': 'OCCIDENTE',
        'oriente': 'ORIENTE',
    }

    username = request.user.username
    if username in user_region_mapping:
        agencias = Agencia.objects.filter(region=user_region_mapping[username])
    else:
        agencias = Agencia.objects.all()

    registros = Registro.objects.all()
    last_update = registros.latest('timestamp').timestamp if registros.exists() else None

    if request.method == 'POST':
        for agencia in agencias:
            Registro.objects.create(
                agencia=agencia.nom_age,
                area='Ventanilla',
                contratados=request.POST.get(f'contratados_vent_{agencia.id_age}', 0),
                conectados=request.POST.get(f'conectados_vent_{agencia.id_age}', 0),
                vacaciones=request.POST.get(f'vacaciones_vent_{agencia.id_age}', 0),
                bajas=request.POST.get(f'bajas_vent_{agencia.id_age}', 0),
                otros_roles=request.POST.get(f'otros_roles_vent_{agencia.id_age}', 0)
            )
            Registro.objects.create(
                agencia=agencia.nom_age,
                area='Plataforma',
                contratados=request.POST.get(f'contratados_plat_{agencia.id_age}', 0),
                conectados=request.POST.get(f'conectados_plat_{agencia.id_age}', 0),
                vacaciones=request.POST.get(f'vacaciones_plat_{agencia.id_age}', 0),
                bajas=request.POST.get(f'bajas_plat_{agencia.id_age}', 0),
                otros_roles=request.POST.get(f'otros_roles_plat_{agencia.id_age}', 0)
            )
        messages.success(request, 'Registro guardado con éxito')

    return render(request, 'form.html', {'agencias': agencias, 'last_update': last_update})

def download_csv(request):
    registros = Registro.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=registros_agencias.csv'

    writer = csv.writer(response)
    writer.writerow(['Agencia', 'Área', 'Contratados', 'Conectados', 'Vacaciones', 'Bajas', 'Otros Roles', 'Timestamp'])
    for registro in registros:
        writer.writerow([registro.agencia, registro.area, registro.contratados, registro.conectados, registro.vacaciones, registro.bajas, registro.otros_roles, registro.timestamp])

    return response
