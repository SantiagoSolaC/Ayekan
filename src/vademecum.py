import sqlite3


# Crear clase 'Medication'.

class Medication:
    def __init__(self, medication_dictionary):
        self.medication_id = medication_dictionary.get('medication_id')
        self.drug_name = medication_dictionary.get('drug_name')
        self.commercial_name = medication_dictionary.get('commercial_name')
        self.pharmaceutical_form = medication_dictionary.get('pharmaceutical_form')
        self.measurement_unit = medication_dictionary.get('measurement_unit')
        self.amount = medication_dictionary.get('amount')

    def to_show_in_html(self):
        self.drug_name = self.drug_name.title()
        self.commercial_name = self.commercial_name.title()
        self.pharmaceutical_form = self.pharmaceutical_form.title()

    def to_store_in_db(self):
        self.drug_name = self.drug_name.lower()
        self.commercial_name = self.commercial_name.lower()
        self.pharmaceutical_form = self.pharmaceutical_form.lower()


# Crear diccionario 'medication' desde tupla.

def create_medication_dictionary(medication_tuple):
    medication_dictionary = {
        "medication_id": medication_tuple[0],
        "drug_name": medication_tuple[1],
        "commercial_name": medication_tuple[2],
        "pharmaceutical_form": medication_tuple[3],
        "measurement_unit": medication_tuple[4],
        "amount": medication_tuple[5]
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
        # if get_medication_by_id(medication.medication_id) == None:
        cursor.execute(f'INSERT INTO vademecum (drug_name, commercial_name, pharmaceutical_form, measurement_unit, amount) VALUES ("{medication.drug_name}", \
        "{medication.commercial_name}", "{medication.pharmaceutical_form}", "{medication.measurement_unit}", "{medication.amount}");')


# Editar un registro de la tabla a partir de su ID.

def edit_db_medication(medication_dictionary):
    medication = Medication(medication_dictionary)
    medication.to_store_in_db()
    with sqlite3.connect("./ayekan.db") as conn:
        cursor = conn.cursor()
        cursor.execute(f'UPDATE vademecum SET drug_name="{medication.drug_name}", commercial_name="{medication.commercial_name}", pharmaceutical_form="{medication.pharmaceutical_form}", \
        measurement_unit="{medication.measurement_unit}", amount="{medication.amount}" WHERE medication_id="{medication.medication_id}";')


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
            medications_list.append(medication)
        return medications_list
