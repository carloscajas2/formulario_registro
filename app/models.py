from django.db import models

class Agencia(models.Model):
    id_age = models.IntegerField(primary_key=True)
    nom_age = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=50)
    region = models.CharField(max_length=50)

class Registro(models.Model):
    agencia = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    contratados = models.IntegerField()
    conectados = models.IntegerField()
    vacaciones = models.IntegerField()
    bajas = models.IntegerField()
    otros_roles = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
