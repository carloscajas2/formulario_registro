from django.db import models

class Agencia(models.Model):
    id_age = models.IntegerField(primary_key=True)
    nom_age = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=50)
    region = models.CharField(max_length=50)

class Registro(models.Model):
    agencia = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    contratados = models.IntegerField(default=0)
    conectados = models.IntegerField(default=0)
    vacaciones = models.IntegerField(default=0)
    nuevos = models.IntegerField(default=0)  # Nuevo campo con valor predeterminado
    bajas_medicas = models.IntegerField(default=0)  # Nuevo campo con valor predeterminado
    remplazo_plataforma_rac = models.IntegerField(default=0)  # Nuevo campo con valor predeterminado
    externas_y_autobancos = models.IntegerField(default=0)  # Nuevo campo con valor predeterminado
    promotor_offline = models.IntegerField(default=0)  # Nuevo campo con valor predeterminado
    timestamp = models.DateTimeField(auto_now_add=True)
