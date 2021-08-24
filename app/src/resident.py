import sqlite3
import time

from app import db


# Crear clase 'Resident'.

# class Resident(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     status = db.Column(db.Boolean, nullable = False)
#     admission_date = db.Column(db.DateTime(timezone = True), nullable = False, default = time.strftime("%Y-%m-%d"))
#     nickname = db.Column(db.String(50))
#     name = db.Column(db.String(50), nullable = False)
#     last_name = db.Column(db.String(50), nullable = False)
#     birth_date = db.Column(db.DateTime(timezone = True), nullable = False)
#     age = db.Column(db.Integer, nullable = False) 
#     gender = db.Column(db.String(50), nullable = False)
#     citizenship = db.Column(db.String(50))
#     marital_status = db.Column(db.String(50))
#     address = db.Column(db.String(100), nullable = False)
#     city = db.Column(db.String(100), nullable = False)
#     id_type = db.Column(db.String(50), nullable = False)
#     id_number = db.Column(db.String(50), nullable = False)
#     prepaid = db.Column(db.String(100))
#     affiliation_number = db.Column(db.String(100))


# Convertir diccionario en instancia.

# def resident_dictionary_to_instance(resident_dictionary):
#     id = resident_dictionary.get("id")
#     status = resident_dictionary.get("status")
#     admission_date = resident_dictionary.get("admission_date")
#     nickname = resident_dictionary.get("nickname")
#     name = resident_dictionary.get("name")
#     last_name = resident_dictionary.get("last_name")
#     birth_date = resident_dictionary.get("birth_date")
#     age = resident_dictionary.get("age")
#     gender = resident_dictionary.get("gender")
#     citizenship = resident_dictionary.get("citizenship")
#     marital_status = resident_dictionary.get("marital_status")
#     address = resident_dictionary.get("address")
#     city = resident_dictionary.get("city")
#     id_type = resident_dictionary.get("id_type")
#     id_number = resident_dictionary.get("id_number")
#     prepaid = resident_dictionary.get("prepaid")
#     affiliation_number = resident_dictionary.get("affiliation_number")
#     resident = Resident(id, status, admission_date, nickname, name, last_name, birth_date, age, gender, citizenship, marital_status, address, city, id_type, id_number,
#         prepaid, affiliation_number)
#     return resident


#     def to_show_in_html(self):
#         self.status = self.status.title()
#         self.name = self.name.title()
#         self.last_name = self.last_name.title()
#         self.gender = self.gender.title()
#         self.citizenship = self.citizenship.title()
#         self.marital_status = self.marital_status.title()
#         self.address = self.address.title()
#         self.city = self.city.title()
#         self.id_type = self.id_type.upper()
#         self.prepaid = self.prepaid.upper()
#         self.nickname = self.nickname.upper()

#     def to_store_in_db(self):
#         self.status = self.status.lower()
#         self.name = self.name.lower()
#         self.last_name = self.last_name.lower()
#         self.gender = self.gender.lower()
#         self.citizenship = self.citizenship.lower()
#         self.marital_status = self.marital_status.lower()
#         self.address = self.address.lower()
#         self.city = self.city.lower()
#         self.id_type = self.id_type.lower()
#         self.prepaid = self.prepaid.lower()
#         self.nickname = self.nickname.lower()
        
# Crear diccionario 'resident' desde tupla.


# def create_resident_dictionary(resident_tuple):
#     resident_dictionary = {
#         "resident_id" : resident_tuple[0],
#         "name" : resident_tuple[1],
#         "last_name" : resident_tuple[2],
#         "status" : resident_tuple[3],
#         "admission_date" : resident_tuple[4],
#         "birth_date" : resident_tuple[5],
#         "age" : resident_tuple[6],
#         "gender" : resident_tuple[7],
#         "citizenship" : resident_tuple[8],
#         "marital_status" : resident_tuple[9],
#         "id_type" : resident_tuple[10],
#         "id_number" : resident_tuple[11],
#         "address" : resident_tuple[12],
#         "city" : resident_tuple[13],
#         "prepaid" : resident_tuple[14],
#         "affiliation_number" : resident_tuple[15],
#         "nickname" : resident_tuple[16]
#     }
#     return resident_dictionary
        

# Buscar residente por numero de DNI. Devuelve instancia.

# def get_resident_by_id(id):
#     resident = Resident.query.get(id)
#     return resident

    
# # Buscar residente por un campo dado. Recibe parámetro campo y valor. Devuelve una lista de instancias.

# def get_resident_list_by_value(field_name, value):
#     resident_list = Resident.query.filter(Resident.field_name.like(f"{value}")).all()
#     return resident_list

    
# # Buscar residente por un campo dado. Recibe parámetro campo y valor. Devuelve una instancia.

# def get_resident_by_value(field_name, value):
#     resident = Resident.query.filter(Resident.field_name.like(f"{value}")).first()
#     return resident


# # Crear un nuevo registro en las tablas 'residents' y 'residents_registry'. Recibe un diccionario.


# def create_new_resident(resident_dictionary):
#     resident = Resident(resident_dictionary)
#     resident.to_store_in_db()
#     with sqlite3.connect("./ayekan.db") as conn:
#         cursor = conn.cursor()
#         if get_resident_by_id(resident.id_number) == None:
#             cursor.executescript(f'INSERT INTO residents_registry (type, resident_id, name, last_name, status, admission_date, birth_date, age, gender, citizenship, marital_status, \
#             id_type, id_number, address, city, prepaid, affiliation_number, nickname, registry_date) VALUES ("creation", "{resident.resident_id}", "{resident.name}", \
#             "{resident.last_name}", "{resident.status}", "{resident.admission_date}", "{resident.birth_date}", "{resident.age}", "{resident.gender}", "{resident.citizenship}", \
#             "{resident.marital_status}", "{resident.id_type}", "{resident.id_number}", "{resident.address}", "{resident.city}", "{resident.prepaid}", "{resident.affiliation_number}", \
#             "{resident.nickname}", "{time.strftime("%Y-%m-%d")}"); \
#             INSERT INTO residents (name, last_name, status, admission_date, birth_date, age, gender, citizenship, marital_status, id_type, id_number, address, city, \
#             prepaid, affiliation_number, nickname) VALUES ("{resident.name}", "{resident.last_name}", "{resident.status}", "{resident.admission_date}", "{resident.birth_date}", \
#             "{resident.age}", "{resident.gender}", "{resident.citizenship}", "{resident.marital_status}", "{resident.id_type}", "{resident.id_number}", "{resident.address}", \
#             "{resident.city}", "{resident.prepaid}", "{resident.affiliation_number}", "{resident.nickname}");')
        
# # Editar un registro de la tabla a partir de su ID. Crea entrada en la tabla 'residents_registry'. Recibe un diccionario.


# def edit_db_resident(resident_dictionary):
#     resident = Resident(resident_dictionary)
#     resident.to_store_in_db()
#     with sqlite3.connect("./ayekan.db") as conn:
#         cursor = conn.cursor()
#         cursor.executescript(f'INSERT INTO residents_registry (type, resident_id, name, last_name, status, admission_date, birth_date, age, gender, citizenship, marital_status, \
#             id_type, id_number, address, city, prepaid, affiliation_number, nickname, registry_date) VALUES ("modification", "{resident.resident_id}", "{resident.name}", \
#             "{resident.last_name}", "{resident.status}", "{resident.admission_date}", "{resident.birth_date}", "{resident.age}", "{resident.gender}", "{resident.citizenship}", \
#             "{resident.marital_status}", "{resident.id_type}", "{resident.id_number}", "{resident.address}", "{resident.city}", "{resident.prepaid}", "{resident.affiliation_number}", \
#             "{resident.nickname}", "{time.strftime("%Y-%m-%d")}"); \
#             UPDATE residents SET name="{resident.name}", last_name="{resident.last_name}", status="{resident.status}", admission_date="{resident.admission_date}", \
#             birth_date="{resident.birth_date}", age="{resident.age}", gender="{resident.gender}", citizenship="{resident.citizenship}", marital_status="{resident.marital_status}", \
#             id_type="{resident.id_type}", id_number="{resident.id_number}", address="{resident.address}", city="{resident.city}", prepaid="{resident.prepaid}", \
#             affiliation_number="{resident.affiliation_number}", nickname="{resident.nickname}" WHERE resident_id={resident.resident_id};')

# # Listar todos los residentes. Devuelve lista de instancias.


# def get_residents_list():
    # with sqlite3.connect("./ayekan.db") as conn:
    #     cursor = conn.cursor()
    #     cursor.execute(f"SELECT * FROM residents;")
    #     result = cursor.fetchall()
    #     residents_list = []
    #     for resident in result:
    #         resident_dictionary = create_resident_dictionary(resident)
    #         resident = Resident(resident_dictionary)
    #         residents_list.append(resident)
    #     return residents_list