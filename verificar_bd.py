import sqlite3

# Ruta a tu base de datos SQLite
database_path = 'db.sqlite3'

# Conectar a la base de datos
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Verificar si la tabla agencia existe
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='app_agencia';")
table_exists = cursor.fetchone()

if table_exists:
    print("La tabla 'app_agencia' existe.")
    
    # Listar contenido de la tabla agencia
    cursor.execute("SELECT * FROM app_agencia;")
    rows = cursor.fetchall()
    
    for row in rows:
        print(row)
else:
    print("La tabla 'app_agencia' no existe.")

# Cerrar la conexión
conn.close()
