import sqlite3
import time

# Crear clase 'Medication'.


class Medication:
    def __init__(self, medication_dictionary):
        self.medication_id = medication_dictionary.get('medication_id')
        self.drug_name = medication_dictionary.get('drug_name')
        self.commercial_name = medication_dictionary.get('commercial_name')
        self.type = medication_dictionary.get('type')
        self.measurement_unit = medication_dictionary.get('measurement_unit')
        self.amount = medication_dictionary.get('amount')
        self.registration_date = medication_dictionary.get('registration_date')

    def to_show_in_html(self):
        self.drug_name = self.drug_name.title()
        self.commercial_name = self.commercial_name.title()
        self.type = self.type.title()
        # self.measurement_unit = self.measurement_unit.upper()

    def to_store_in_db(self):
        self.drug_name = self.drug_name.lower()
        self.commercial_name = self.commercial_name.lower()
        self.type = self.type.lower()
        self.measurement_unit = self.measurement_unit.lower()

# Crear diccionario 'medication' desde tupla.


def create_medication_dictionary(medication_tuple):
    medication_dictionary = {
        "medication_id": medication_tuple[0],
        "drug_name": medication_tuple[1],
        "commercial_name": medication_tuple[2],
        "type": medication_tuple[3],
        "measurement_unit": medication_tuple[4],
        "amount": medication_tuple[5],
        "registration_date": medication_tuple[6]
    }
    return medication_dictionary

# Buscar medicación por numero de ID. Devuelve instancia.


def get_medication_by_id(medication_id):
    with sqlite3.connect("./ayekan.db") as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM vademecum WHERE medication_id="{medication_id}";')
        result = cursor.fetchone()
        medication_dictionary = create_medication_dictionary(result)
        medication = Medication(medication_dictionary)
        return medication

# Buscar medicación por un campo dado. Recibe parámetro campo y valor. Devuelve lista de instancias.


def get_medication_by_value(field_name, value):
    with sqlite3.connect("./ayekan.db") as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM vademecum WHERE {field_name} LIKE "%{value}%";')
        result = cursor.fetchone()
        medication_dictionary = create_medication_dictionary(result)
        medication = Medication(medication_dictionary)
        return medication
    
# Buscar medicación por un campo dado. Recibe parámetro campo y valor. Devuelve lista de instancias.


def get_medication_list_by_value(field_name, value):
    with sqlite3.connect("./ayekan.db") as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM vademecum WHERE {field_name} LIKE "%{value}%";')
        result = cursor.fetchall()
        medications_list = []
        for medication_tuple in result:
            medication_dictionary = create_medication_dictionary(medication_tuple)
            medication = Medication(medication_dictionary)
            medications_list.append(medication)
        return medications_list

# Crear un nuevo registro en la tabla.


def create_new_medication(medication_dictionary):
    medication = Medication(medication_dictionary)
    medication.to_store_in_db()
    with sqlite3.connect("./ayekan.db") as conn:
        cursor = conn.cursor()
        if get_medication_by_id(medication.medication_id) == None:
            cursor.execute(f'INSERT INTO vademecum (drug_name, commercial_name, type, measurement_unit, amount, registration_date) VALUES ("{medication.drug_name}", \
            "{medication.commercial_name}", "{medication.type}", "{medication.measurement_unit}", "{medication.amount}", "{time.strftime("%Y-%m-%d")}");')

# Editar un registro de la tabla a partir de su ID.


def edit_db_medication(medication_dictionary):
    medication = Medication(medication_dictionary)
    medication.to_store_in_db()
    with sqlite3.connect("./ayekan.db") as conn:
        cursor = conn.cursor()
        cursor.execute(f'UPDATE vademecum SET drug_name="{medication.drug_name}", commercial_name="{medication.commercial_name}", type="{medication.type}", \
        measurement_unit="{medication.measurement_unit}", amount="{medication.amount}", registration_date="{medication.registration_date}" \
        WHERE medication_id="{medication.medication_id}";')

# Listar todas las medicaciones. Devuelve lista de instancias.


def get_medications_list():
    with sqlite3.connect("./ayekan.db") as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM vademecum ORDER BY commercial_name;")
        result = cursor.fetchall()
        medications_list = []
        for medication in result:
            medication_dictionary = create_medication_dictionary(medication)
            medication = Medication(medication_dictionary)
            medication.to_show_in_html()
            medications_list.append(medication)
        return medications_list
