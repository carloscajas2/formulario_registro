from django.core.management.base import BaseCommand
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Popula la tabla agencia desde un archivo SQL'

    def handle(self, *args, **kwargs):
        script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'populate_agencias.sql')
        with open(script_path, 'r') as file:
            sql = file.read()
            with connection.cursor() as cursor:
                cursor.executescript(sql)
        self.stdout.write(self.style.SUCCESS('Datos de agencias insertados correctamente'))
