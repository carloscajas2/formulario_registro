from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import Agencia, Registro
import csv
from io import StringIO


def some_view(request):
    user_name = request.user.username  # Asegúrate de que el usuario esté autenticado
    context = {
        'user_name': user_name,
        'last_update': '2024-08-02',  # Ejemplo, debería ser dinámico
        'agencias_datos': [],  # Otros datos necesarios para la plantilla
        'messages': [],  # Otros mensajes necesarios para la plantilla
    }
    return render(request, 'template.html', context)


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

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Agencia, Registro  # Asegúrate de importar los modelos correctos

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

    agencias_datos = []
    for agencia in agencias:
        data = {
            'agencia': agencia,
            'ventanilla': {
                'contratados': 0, 'conectados': 0, 'vacaciones': 0, 'bajas': 0, 'otros_roles': 0
            },
            'plataforma': {
                'contratados': 0, 'conectados': 0, 'vacaciones': 0, 'bajas': 0, 'otros_roles': 0
            }
        }
        ventanilla = Registro.objects.filter(agencia=agencia.nom_age, area='Ventanilla').order_by('-timestamp').first()
        plataforma = Registro.objects.filter(agencia=agencia.nom_age, area='Plataforma').order_by('-timestamp').first()
        
        if ventanilla:
            data['ventanilla'].update({
                'contratados': ventanilla.contratados,
                'conectados': ventanilla.conectados,
                'vacaciones': ventanilla.vacaciones,
                'bajas': ventanilla.bajas,
                'otros_roles': ventanilla.otros_roles
            })
        
        if plataforma:
            data['plataforma'].update({
                'contratados': plataforma.contratados,
                'conectados': plataforma.conectados,
                'vacaciones': plataforma.vacaciones,
                'bajas': plataforma.bajas,
                'otros_roles': plataforma.otros_roles
            })
        
        agencias_datos.append(data)

    if request.method == 'POST':
        for data in agencias_datos:
            Registro.objects.create(
                agencia=data['agencia'].nom_age,
                area='Ventanilla',
                contratados=request.POST.get(f'contratados_vent_{data['agencia'].id_age}', 0),
                conectados=request.POST.get(f'conectados_vent_{data['agencia'].id_age}', 0),
                vacaciones=request.POST.get(f'vacaciones_vent_{data['agencia'].id_age}', 0),
                bajas=request.POST.get(f'bajas_vent_{data['agencia'].id_age}', 0),
                otros_roles=request.POST.get(f'otros_roles_vent_{data['agencia'].id_age}', 0)
            )
            Registro.objects.create(
                agencia=data['agencia'].nom_age,
                area='Plataforma',
                contratados=request.POST.get(f'contratados_plat_{data['agencia'].id_age}', 0),
                conectados=request.POST.get(f'conectados_plat_{data['agencia'].id_age}', 0),
                vacaciones=request.POST.get(f'vacaciones_plat_{data['agencia'].id_age}', 0),
                bajas=request.POST.get(f'bajas_plat_{data['agencia'].id_age}', 0),
                otros_roles=request.POST.get(f'otros_roles_plat_{data['agencia'].id_age}', 0)
            )
        messages.success(request, 'Registro guardado con éxito')

    return render(request, 'form.html', {
        'agencias_datos': agencias_datos,
        'last_update': Registro.objects.latest('timestamp').timestamp if Registro.objects.exists() else None
    })

def download_csv(request):
    registros = Registro.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=registros_agencias.csv'

    writer = csv.writer(response)
    writer.writerow(['Agencia', 'Área', 'Contratados', 'Conectados', 'Vacaciones', 'Bajas', 'Otros Roles', 'Timestamp'])
    for registro in registros:
        writer.writerow([registro.agencia, registro.area, registro.contratados, registro.conectados, registro.vacaciones, registro.bajas, registro.otros_roles, registro.timestamp])

    return response
