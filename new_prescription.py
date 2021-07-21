from new_resident import Resident
from new_medication import Medication
import sqlite3
connection = sqlite3.connect('ayekan.db')
cursor = connection.cursor()

# Crear clase 'Prescription'.

class Prescription:
    def __init__(self, prescription_tuple):
        self.id = prescription_tuple[0]
        self.resident_id = prescription_tuple[1]
        self.medication_id = prescription_tuple[2]
        self.administration_route = prescription_tuple[3]
        self.breakfast = prescription_tuple[4]
        self.lunch = prescription_tuple[5]
        self.tea = prescription_tuple[6]
        self.dinner = prescription_tuple[7]
        self.total_per_day = prescription_tuple[8]
        self.stock = prescription_tuple[9]
        self.days_left = prescription_tuple[10]
        self.notes = prescription_tuple[11]
        self.medication_status = prescription_tuple[12]
        self.prescription_date = prescription_tuple[13]
        self.last_registry_date = prescription_tuple[14]
        self.in_pillbox = prescription_tuple[15]
        self.floor = prescription_tuple[16]
        self.resident_status = prescription_tuple[17]


# Buscar residentes por nombre y reemplazar por su ID.

def replace_resident_name_for_id():
    cursor.execute(f'SELECT * \
        FROM prescriptions;')
    prescriptions_list = cursor.fetchall()
    for prescription_tuple in prescriptions_list:
        prescription = Prescription(prescription_tuple)
        cursor.execute(f'SELECT * \
            FROM residents \
            WHERE last_name \
            LIKE "%{prescription.resident_id}%";')
        resident_tuple = cursor.fetchone()
        if resident_tuple != None:
            resident = Resident(resident_tuple)
            cursor.execute(f'UPDATE prescriptions \
                SET resident_id="{resident.id}" \
                WHERE resident_id="{prescription.resident_id}";')
            connection.commit()

# Buscar medicación por nombre y reemplazar por su ID.

def replace_drug_name_for_id():
    cursor.execute(f'SELECT * \
        FROM prescriptions;')
    prescriptions_list = cursor.fetchall()
    for prescription_tuple in prescriptions_list:
        prescription = Prescription(prescription_tuple)
        cursor.execute(f'SELECT * \
            FROM vademecum \
            WHERE drug_name \
            LIKE "%{prescription.medication_id}%";')
        medication_tuple = cursor.fetchone()
        if medication_tuple != None:
            medication = Medication(medication_tuple)
            cursor.execute(f'UPDATE prescriptions \
                SET medication_id="{medication.id}" \
                WHERE medication_id="{prescription.medication_id}";')
            connection.commit()

# Crear un nuevo registro en la tabla 'prescriptions' y 'prescriptions_registry'.

def insert_new_prescription(prescription_tuple):
    prescription = Prescription(prescription_tuple)
    cursor.execute(f'INSERT INTO prescriptions(\
        resident_id, \
        medication_id, \
        administration_route, \
        breakfast, \
        lunch, \
        tea, \
        dinner, \
        total_per_day, \
        stock, \
        days_left, \
        notes, \
        medication_status, \
        prescription_date, \
        last_registry_date, \
        in_pillbox, \
        floor, \
        resident_status) \
        VALUES ("{prescription.resident_id}", "{prescription.medication_id}", "{prescription.administration_route}", "{prescription.breakfast}", "{prescription.lunch}", \
            "{prescription.tea}", "{prescription.dinner}", "{prescription.total_per_day}", "{prescription.stock}", "{prescription.days_left}", "{prescription.notes}", \
            "{prescription.medication_status}", "{prescription.prescription_date}", "{prescription.last_registry_date}", "{prescription.in_pillbox}", "{prescription.floor}", \
            "{prescription.resident_status}");')
    cursor.execute(f'INSERT INTO prescriptions_registry(\
        resident_id, \
        medication_id, \
        administration_route, \
        breakfast, \
        lunch, \
        tea, \
        dinner, \
        total_per_day, \
        stock, \
        days_left, \
        notes, \
        medication_status, \
        prescription_date, \
        last_registry_date, \
        in_pillbox, \
        floor, \
        resident_status) \
        VALUES ("{prescription.resident_id}", "{prescription.medication_id}", "{prescription.administration_route}", "{prescription.breakfast}", "{prescription.lunch}", \
            "{prescription.tea}", "{prescription.dinner}", "{prescription.total_per_day}", "{prescription.stock}", "{prescription.days_left}", "{prescription.notes}", \
            "{prescription.medication_status}", "{prescription.prescription_date}", "{prescription.last_registry_date}", "{prescription.in_pillbox}", "{prescription.floor}", \
            "{prescription.resident_status}");')
    connection.commit()

# Editar un registro de la tabla a partir de su ID y crear registro en la tabla 'prescriptions_registry'.

def edit_prescription(prescription_tuple):
    prescription = Prescription(prescription_tuple)
    cursor.execute(f'UPDATE prescriptions SET \
        resident_id="{prescription.resident_id}", \
        medication_id="{prescription.medication_id}", \
        administration_route="{prescription.administration_route}", \
        breakfast="{prescription.breakfast}", \
        lunch="{prescription.lunch}", \
        tea="{prescription.tea}", \
        dinner="{prescription.dinner}", \
        total_per_day="{prescription.total_per_day}", \
        stock="{prescription.stock}", \
        days_left="{prescription.days_left}", \
        notes="{prescription.notes}", \
        medication_status="{prescription.medication_status}", \
        prescription_date="{prescription.prescription_date}", \
        last_registry_date="{prescription.last_registry_date}", \
        in_pillbox="{prescription.in_pillbox}", \
        floor="{prescription.floor}", \
        resident_status="{prescription.resident_status}", \
        WHERE id="{prescription.id}";')
    cursor.execute(f'INSERT INTO prescriptions_registry(\
        resident_id, \
        medication_id, \
        administration_route, \
        breakfast, \
        lunch, \
        tea, \
        dinner, \
        total_per_day, \
        stock, \
        days_left, \
        notes, \
        medication_status, \
        prescription_date, \
        last_registry_date, \
        in_pillbox, \
        floor, \
        resident_status) \
        VALUES ("{prescription.resident_id}", "{prescription.medication_id}", "{prescription.administration_route}", "{prescription.breakfast}", "{prescription.lunch}", \
            "{prescription.tea}", "{prescription.dinner}", "{prescription.total_per_day}", "{prescription.stock}", "{prescription.days_left}", "{prescription.notes}", \
            "{prescription.medication_status}", "{prescription.prescription_date}", "{prescription.last_registry_date}", "{prescription.in_pillbox}", "{prescription.floor}", \
            "{prescription.resident_status}");')
    connection.commit()
        
# Eliminar un registro de la tabla a partir de su ID.

def delete_prescription(prescription_tuple):
    prescription = Prescription(prescription_tuple)
    cursor.execute(f'DELETE FROM prescriptions \
        WHERE id="{prescription.id}";')
    connection.commit
        
# Buscar todas las prescripciones por ID de residente. Recibe una tupla, devuelve una lista de tuplas.

def get_prescriptions_by_resident(resident_tuple):
    resident = Resident(resident_tuple)
    cursor.execute(f'SELECT * \
            FROM prescriptions \
            WHERE resident_id="{resident.id}";')
    prescriptions_list = cursor.fetchall()
    return prescriptions_list

connection.close()