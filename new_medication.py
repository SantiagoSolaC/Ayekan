import sqlite3
connection = sqlite3.connect('ayekan.db')
cursor = connection.cursor()

# Crear clase 'Medication'.

class Medication:
    def __init__(self, medication_tuple):
        self.id = medication_tuple[0]
        self.drug_name = medication_tuple[1]
        self.commercial_name = medication_tuple[2]
        self.type = medication_tuple[3]
        self.amount = medication_tuple[4]

        
# Buscar medicación por numero de ID. Devuelve tupla.

def get_medication_by_id(id):
    cursor.execute(f'SELECT * \
        FROM vademecum \
        WHERE id="{id}";')
    result = cursor.fetchone()
    if result != None:
        return result
    else:
        return None
    
# Buscar medicación por nombre de droga o nombre comercial. Devuelve tupla.

def get_medication_by_name(some_name):
    cursor.execute(f'SELECT * \
        FROM vademecum \
        WHERE drug_name \
        LIKE "%{some_name.title()}%" \
        OR commercial_name \
        LIKE "%{some_name.title()}%" \
        OR drug_name \
        LIKE "%{some_name.upper()}%" \
        OR commercial_name \
        LIKE "%{some_name.upper()}%" \
        OR drug_name \
        LIKE "%{some_name.lower()}%" \
        OR commercial_name \
        LIKE "%{some_name.lower()}%";')
    result = cursor.fetchall()
    if result != None:
        return result
    else:
        return None

# Crear un nuevo registro en la tabla.

def insert_medication(medication_tuple):
    medication = Medication(medication_tuple)
    if get_medication_by_id(medication.id) == None:
        cursor.execute(f'INSERT INTO vademecum (\
            drug_name, \
            commercial_name, \
            type, amount) \
            VALUES ("{medication.drug_name}", "{medication.commercial_name}", "{medication.type}", "{medication.amount}");')
        connection.commit()
    else:
        print('Existe un registro con ese número de documento.')
        
# Editar un registro de la tabla a partir de su ID.

def edit_medication(medication_tuple):
    medication = Medication(medication_tuple)
    if len(medication_tuple) == 5:
        cursor.execute(f'UPDATE vademecum SET drug_name="{medication.drug_name}", commercial_name="{medication.commercial_name}", type="{medication.type}", \
            amount="{medication.amount}" WHERE id="{medication.id}";')
        connection.commit()
    else:
        print('Largo de tupla no compatible.')
        
# Eliminar un registro de la tabla a partir de su ID.

def delete_medication(medication_tuple):
    medication = Medication(medication_tuple)
    if len(medication_tuple) == 5:
        cursor.execute(f'DELETE FROM vademecum WHERE id="{medication.id}";')
        connection.commit
    else:
        print('Largo de tupla no compatible.')

connection.close()
