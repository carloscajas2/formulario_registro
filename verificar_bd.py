import sqlite3
import os

def verificar_tablas(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    tablas = ['app_agencia', 'app_registro']

    for tabla in tablas:
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tabla}';")
        result = cursor.fetchone()
        if result:
            print(f"La tabla '{tabla}' existe.")
        else:
            print(f"La tabla '{tabla}' no existe.")

    conn.close()

if __name__ == "__main__":
    db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
    verificar_tablas(db_path)
