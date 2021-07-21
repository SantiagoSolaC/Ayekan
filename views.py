from new_resident import Resident, get_resident_by_name
import sqlite3
connection = sqlite3.connect('ayekan.db')
cursor = connection.cursor()

# Visualizar stock de medicamentos por residente. Recibe tupla y devuelve lista de tuplas.

def view_stock_by_resident(resident_tuple):
    resident = get_resident_by_name(resident_tuple)
    cursor.execute(f'SELECT * \
        FROM residents \
        WHERE resident.id="{resident.id}"')