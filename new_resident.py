import sqlite3
connection = sqlite3.connect('ayekan.db')
cursor = connection.cursor()

# Crear clase 'Resident'.

class Resident:
    def __init__(self, resident_tuple):
        self.id = resident_tuple[0]
        self.name = resident_tuple[1]
        self.last_name = resident_tuple[2]
        self.status = resident_tuple[3]
        self.admission_date = resident_tuple[4]
        self.birth_date = resident_tuple[5]
        self.age = resident_tuple[6]
        self.gender = resident_tuple[7]
        self.citizenship = resident_tuple[8]
        self.marital_status = resident_tuple[9]
        self.id_type = resident_tuple[10]
        self.id_number = resident_tuple[11]
        self.address = resident_tuple[12]
        self.city = resident_tuple[13]
        self.prepaid = resident_tuple[14]
        self.affiliation_number = resident_tuple[15]
        self.nickname = resident_tuple[16]
        
# Buscar residente por numero de DNI. Devuelve tupla.

def get_resident_by_id_number(id_number):
    cursor.execute(f'SELECT * \
        FROM residents \
        WHERE id_number="{id_number}";')
    result = cursor.fetchone()
    if result != None:
        return result
    else:
        return None
    
# Buscar residente por nombre y/o apellido. Devuelve lista de tuplas.

def get_resident_by_name(name):
    cursor.execute(f'SELECT * \
        FROM residents \
        WHERE name \
        LIKE "%{name.title()}%" \
        OR last_name \
        LIKE "%{name.title()}%";')
    result = cursor.fetchall()
    if result != None:
        return result
    else:
        return None
    
# Crear un nuevo registro en la tabla.

def insert_resident(resident_tuple):
    resident = Resident(resident_tuple)
    if get_resident_by_id_number(resident.id_number) == None:
        cursor.execute(f'INSERT INTO residents (\
            name, \
            last_name, \
            status, \
            admission_date, \
            birth_date, \
            age, \
            gender, \
            citizenship, \
            marital_status, \
            id_type, \
            id_number, \
            address, \
            city, \
            prepaid, \
            affiliation_number, \
            nickname) \
            VALUES ("{resident.name}", "{resident.last_name}", "{resident.status}", "{resident.admission_date}", "{resident.birth_date}", "{resident.age}", \
                "{resident.gender}", "{resident.citizenship}", "{resident.marital_status}", "{resident.id_type}", "{resident.id_number}", "{resident.address}", \
                "{resident.city}", "{resident.prepaid}", "{resident.affiliation_number}", "{resident.nickname}");')
        connection.commit()
    else:
        print('Existe un registro con ese número de documento.')
        
# Editar un registro de la tabla a partir de su ID.

def edit_resident(resident_tuple):
    resident = Resident(resident_tuple)
    if len(resident_tuple) == 17:
        cursor.execute(f'UPDATE residents SET \
            name="{resident.name}", \
            last_name="{resident.last_name}", \
            status="{resident.status}", \
            admission_date="{resident.admission_date}", \
            birth_date="{resident.birth_date}", \
            age="{resident.age}", \
            gender="{resident.gender}", \
            citizenship="{resident.citizenship}", \
            marital_status="{resident.marital_status}", \
            id_type="{resident.marital_status}", \
            id_number="{resident.id_number}", \
            address="{resident.address}", \
            city="{resident.city}", \
            prepaid="{resident.prepaid}", \
            affiliation_number="{resident.affiliation_number}", \
            nickname="{resident.nickname}" \
            WHERE id="{resident.id}";')
        connection.commit()
    else:
        print('Largo de tupla no compatible.')
        
# Eliminar un registro de la tabla a partir de su ID.

def delete_resident(resident_tuple):
    resident = Resident(resident_tuple)
    if len(resident_tuple) == 17:
        cursor.execute(f'DELETE FROM residents \
            WHERE id="{resident.id}";')
        connection.commit
    else:
        print('Largo de tupla no compatible.')

connection.close()