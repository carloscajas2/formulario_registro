from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import Agencia, Registro
import csv

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

    agencias_datos = []
    for agencia in agencias:
        data = {
            'agencia': agencia,
            'ventanilla': {
                'Contratados': 0, 'Conectados': 0, 'Nuevos': 0, 'Bajas Medicas': 0, 'Remplazo Plataforma/RAC': 0,
                'Externas y Autobancos': 0, 'Promotor Offline': 0
            },
            'plataforma': {
                'Contratados': 0, 'Conectados': 0, 'Nuevos': 0, 'Bajas Medicas': 0, 'Remplazo Plataforma/RAC': 0,
                'Externas y Autobancos': 0, 'Promotor Offline': 0
            }
        }
        ventanilla = Registro.objects.filter(agencia=agencia.nom_age, area='Ventanilla').order_by('-timestamp').first()
        plataforma = Registro.objects.filter(agencia=agencia.nom_age, area='Plataforma').order_by('-timestamp').first()

        if ventanilla:
            data['ventanilla'].update({
                'Contratados': ventanilla.contratados,
                'Conectados': ventanilla.conectados,
                'Nuevos': ventanilla.nuevos,
                'Bajas Medicas': ventanilla.bajas_medicas,
                'Remplazo Plataforma/RAC': ventanilla.remplazo_plataforma_rac,
                'Externas y Autobancos': ventanilla.externas_y_autobancos,
                'Promotor Offline': ventanilla.promotor_offline
            })

        if plataforma:
            data['plataforma'].update({
                'Contratados': plataforma.contratados,
                'Conectados': plataforma.conectados,
                'Nuevos': plataforma.nuevos,
                'Bajas Medicas': plataforma.bajas_medicas,
                'Remplazo Plataforma/RAC': plataforma.remplazo_plataforma_rac,
                'Externas y Autobancos': plataforma.externas_y_autobancos,
                'Promotor Offline': plataforma.promotor_offline
            })

        agencias_datos.append(data)

    if request.method == 'POST':
        for data in agencias_datos:
            Registro.objects.create(
                agencia=data['agencia'].nom_age,
                area='Ventanilla',
                contratados=request.POST.get(f'contratados_vent_{data["agencia"].id_age}', 0),
                conectados=request.POST.get(f'conectados_vent_{data["agencia"].id_age}', 0),
                nuevos=request.POST.get(f'nuevos_vent_{data["agencia"].id_age}', 0),
                bajas_medicas=request.POST.get(f'bajas_medicas_vent_{data["agencia"].id_age}', 0),
                remplazo_plataforma_rac=request.POST.get(f'remplazo_plataforma_rac_vent_{data["agencia"].id_age}', 0),
                externas_y_autobancos=request.POST.get(f'externas_y_autobancos_vent_{data["agencia"].id_age}', 0),
                promotor_offline=request.POST.get(f'promotor_offline_vent_{data["agencia"].id_age}', 0)
            )
            Registro.objects.create(
                agencia=data['agencia'].nom_age,
                area='Plataforma',
                contratados=request.POST.get(f'contratados_plat_{data["agencia"].id_age}', 0),
                conectados=request.POST.get(f'conectados_plat_{data["agencia"].id_age}', 0),
                nuevos=request.POST.get(f'nuevos_plat_{data["agencia"].id_age}', 0),
                bajas_medicas=request.POST.get(f'bajas_medicas_plat_{data["agencia"].id_age}', 0),
                remplazo_plataforma_rac=request.POST.get(f'remplazo_plataforma_rac_plat_{data["agencia"].id_age}', 0),
                externas_y_autobancos=request.POST.get(f'externas_y_autobancos_plat_{data["agencia"].id_age}', 0),
                promotor_offline=request.POST.get(f'promotor_offline_plat_{data["agencia"].id_age}', 0)
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
    writer.writerow(
        ['Agencia', 'Área', 'Contratados', 'Conectados', 'Nuevos', 'Bajas Medicas', 'Remplazo Plataforma/RAC',
         'Externas y Autobancos', 'Promotor Offline', 'Timestamp'])
    for registro in registros:
        writer.writerow([registro.agencia, registro.area, registro.contratados, registro.conectados, registro.nuevos,
                         registro.bajas_medicas, registro.remplazo_plataforma_rac, registro.externas_y_autobancos,
                         registro.promotor_offline, registro.timestamp])

    return response
