from src.resident import get_resident_by_id, get_resident_by_value
from src.medication import get_medication_by_id
from src.stock import get_stock_from_value, get_stock_list
import sqlite3
import time

# Crear clase 'Prescription'.


class Prescription:
    def __init__(self, prescription_dictionary):
        self.prescription_id = prescription_dictionary.get('prescription_id')
        self.resident_id = prescription_dictionary.get('resident_id')
        self.medication_id = prescription_dictionary.get('medication_id')
        self.administration_route = prescription_dictionary.get('administration_route')
        self.breakfast = prescription_dictionary.get('breakfast')
        self.lunch = prescription_dictionary.get('lunch')
        self.tea = prescription_dictionary.get('tea')
        self.dinner = prescription_dictionary.get('dinner')
        self.total_per_day = prescription_dictionary.get('total_per_day')
        self.notes = prescription_dictionary.get('notes')
        self.medication_status = prescription_dictionary.get('medication_status')
        self.prescription_date = prescription_dictionary.get('prescription_date')
        self.last_registry_date = prescription_dictionary.get('last_registry_date')
        self.in_pillbox = prescription_dictionary.get('in_pillbox')
        self.floor = prescription_dictionary.get('floor')

    def to_show_in_html(self):
        self.resident_id = get_resident_by_id(self.resident_id).nickname.upper()
        self.medication_id = get_medication_by_id(self.medication_id).commercial_name.title()
        self.administration_route = self.administration_route.title()
        total_per_day = self.breakfast + self.lunch + self.tea + self.dinner
        self.total_per_day = total_per_day
        self.medication_status = self.medication_status.title()
        if self.in_pillbox == 1:
            in_pillbox = "SI"
        elif self.in_pillbox == 0:
            in_pillbox = "NO"
        self.in_pillbox = in_pillbox
        self.floor = self.floor.upper()
        
    def to_store_in_db(self):
        self.resident_id = get_resident_by_value("nickname", self.resident_id).resident_id
        self.administration_route = self.administration_route.lower()
        self.medication_status = self.medication_status.lower()
        if self.in_pillbox == "SI":
            in_pillbox = 1
        else:
            in_pillbox = 0
        self.in_pillbox = in_pillbox
        self.floor = self.floor.lower()
        
    def days_left(self):
        stock_list = get_stock_from_value("prescription_id", self.prescription_id)
        stock_amount = 0
        for stock in stock_list:
            stock_amount += stock.amount
        if stock_amount > 0:
            days_left = stock_amount / self.total_per_day
            return days_left

# Crear diccionario 'prescription' desde tupla.


def create_prescription_dictionary(prescription_tuple):
    prescription_dictionary = {
        "prescription_id": prescription_tuple[0],
        "resident_id": prescription_tuple[1],
        "medication_id": prescription_tuple[2],
        "administration_route": prescription_tuple[3],
        "breakfast": prescription_tuple[4],
        "lunch": prescription_tuple[5],
        "tea": prescription_tuple[6],
        "dinner": prescription_tuple[7],
        "total_per_day": prescription_tuple[8],
        "notes": prescription_tuple[9],
        "medication_status": prescription_tuple[10],
        "prescription_date": prescription_tuple[11],
        "last_registry_date": prescription_tuple[12],
        "in_pillbox": prescription_tuple[13],
        "floor": prescription_tuple[14],
    }
    return prescription_dictionary

# Buscar prescripción por numero de ID. Devuelve instancia.


def get_prescription_by_id(prescription_id):
    with sqlite3.connect("./ayekan.db") as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM prescriptions WHERE prescription_id="{prescription_id}";')
        result = cursor.fetchone()
        prescription_dictionary = create_prescription_dictionary(result)
        prescription = Prescription(prescription_dictionary)
        return prescription

# Buscar una prescripción por un campo dado. Recibe parámetro campo y valor. Devuelve lista de instancias.


def get_prescription_by_value(field_name, value):
    with sqlite3.connect("./ayekan.db") as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM prescriptions WHERE {field_name} LIKE "%{value}%";')
        result = cursor.fetchall()
        prescriptions_list = []
        for prescription_tuple in result:
            prescription_dictionary = create_prescription_dictionary(prescription_tuple)
            prescription = Prescription(prescription_dictionary)
            prescriptions_list.append(prescription)
        return prescriptions_list

# Crear un nuevo registro en las tablas 'prescriptions' y 'prescriptions_registry'. Recibe un diccionario.


def create_new_prescription(prescription_dictionary):
    prescription = Prescription(prescription_dictionary)
    prescription.to_store_in_db()
    with sqlite3.connect("./ayekan.db") as conn:
        cursor = conn.cursor()
        if get_prescription_by_id(prescription.prescription_id) == None:
            cursor.executescript(f'INSERT INTO prescriptions (resident_id, medication_id, administration_route, breakfast, lunch, tea, dinner, total_per_day, \
            notes, medication_status, prescription_date, last_registry_date, in_pillbox, floor) VALUES ("{prescription.resident_id}", \
            "{prescription.medication_id}", "{prescription.administration_route}", "{prescription.breakfast}", "{prescription.lunch}", "{prescription.tea}", \
            "{prescription.dinner}", "{prescription.total_per_day}", "{prescription.notes}", \
            "{prescription.medication_status}", "{prescription.prescription_date}", "{prescription.last_registry_date}", "{prescription.in_pillbox}", "{prescription.floor}"; \
            INSERT INTO prescriptions_registry (type, resident_id, medication_id, administration_route, breakfast, lunch, tea, dinner, total_per_day, \
            notes, medication_status, prescription_date, last_registry_date, in_pillbox, floor, registry_date) VALUES ("creation", \
            "{prescription.resident_id}", "{prescription.medication_id}", "{prescription.administration_route}", "{prescription.breakfast}", "{prescription.lunch}", \
            "{prescription.tea}", "{prescription.dinner}", "{prescription.total_per_day}", "{prescription.notes}", \
            "{prescription.medication_status}", "{prescription.prescription_date}", "{prescription.last_registry_date}", "{prescription.in_pillbox}", "{prescription.floor}", \
            "{time.strftime("%Y-%m-%d")}");')

# Editar un registro de la tabla a partir de su ID. Crea entrada en la tabla 'prescriptions_registry'. Recibe un diccionario.


def edit_db_prescription(prescription_dictionary):
    prescription = Prescription(prescription_dictionary)
    prescription.to_store_in_db()
    with sqlite3.connect("./ayekan.db") as conn:
        cursor = conn.cursor()
        cursor.executescript(f'UPDATE prescriptions SET resident_id = "{prescription.resident_id}", medication_id = "{prescription.medication_id}", \
        administration_route = "{prescription.administration_route}", breakfast = "{prescription.breakfast}", lunch = "{prescription.lunch}", tea = "{prescription.tea}", \
        dinner = "{prescription.dinner}", total_per_day = "{prescription.total_per_day}", notes = "{prescription.notes}", \
        medication_status = "{prescription.medication_status}", prescription_date = "{prescription.prescription_date}", \
        last_registry_date = "{prescription.last_registry_date}", in_pillbox = "{prescription.in_pillbox}", floor = "{prescription.floor}" \
        WHERE prescription_id = "{prescription.prescription_id}"; \
        INSERT INTO prescriptions_registry (type, prescription_id, resident_id, medication_id, administration_route, breakfast, lunch, tea, dinner, total_per_day, \
        notes, medication_status, prescription_date, last_registry_date, in_pillbox, floor, registry_date) VALUES ("modification", "{prescription.prescription_id}", \
        "{prescription.resident_id}", "{prescription.medication_id}", "{prescription.administration_route}", "{prescription.breakfast}", "{prescription.lunch}", \
        "{prescription.tea}", "{prescription.dinner}", "{prescription.total_per_day}", "{prescription.notes}", "{prescription.medication_status}", \
        "{prescription.prescription_date}", "{prescription.last_registry_date}", "{prescription.in_pillbox}", "{prescription.floor}", "{time.strftime("%Y-%m-%d")}");')

# Listar todas las prescripciones. Devuelve lista de instancias.


def get_prescriptions_list():
    with sqlite3.connect("./ayekan.db") as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM prescriptions;")
        result = cursor.fetchall()
        prescriptions_list = []
        for prescription in result:
            prescription_dictionary = create_prescription_dictionary(prescription)
            prescription = Prescription(prescription_dictionary)
            prescriptions_list.append(prescription)
        return prescriptions_list
