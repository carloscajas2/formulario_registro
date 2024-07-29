import sqlite3
import csv
import os

def export_to_csv(db_path, output_csv):
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ejecutar la consulta para obtener los datos deseados
    query = """
    SELECT 
        a.id_age, 
        a.ciudad, 
        a.region, 
        r.area, 
        r.contratados, 
        r.conectados, 
        r.vacaciones, 
        r.bajas, 
        r.otros_roles, 
        r.timestamp 
    FROM app_agencia a
    JOIN app_registro r ON a.nom_age = r.agencia
    ORDER BY r.timestamp DESC
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    # Especificar la ruta completa del archivo CSV
    output_csv_path = os.path.join(os.path.dirname(__file__), output_csv)

    # Escribir los datos en el archivo CSV
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Escribir los encabezados
        csvwriter.writerow([
            'id_age', 'ciudad', 'region', 'area', 'contratados', 
            'conectados', 'vacaciones', 'bajas', 'otros_roles', 'timestamp'
        ])
        # Escribir las filas de datos
        csvwriter.writerows(rows)

    # Cerrar la conexión a la base de datos
    conn.close()

    print(f"Datos exportados exitosamente a {output_csv_path}")

if __name__ == "__main__":
    # Especifica la ruta a tu base de datos SQLite
    db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
    # Nombre del archivo CSV de salida
    output_csv = 'registros_agencias.csv'
    export_to_csv(db_path, output_csv)
