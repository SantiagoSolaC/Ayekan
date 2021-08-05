import csv, sqlite3
connection = sqlite3.connect('ayekan.db')
cursor = connection.cursor()

# Crear tabla 'residents' con todas las columnas.

def create_residents_table():
    cursor.execute('CREATE TABLE IF NOT EXISTS residents(\
        id INTEGER PRIMARY KEY AUTOINCREMENT, \
        name CHAR(20) NOT NULL, \
        last_name CHAR(20) NOT NULL, \
        status CHAR(10) NOT NULL, \
        admission_date DATE NOT NULL, \
        birth_date DATE, \
        age CHAR(3), \
        gender CHAR(10) NOT NULL, \
        citizenship CHAR(20), \
        marital_status CHAR(20), \
        id_type CHAR(10) NOT NULL, \
        id_number CHAR(10) NOT NULL, \
        address CHAR(30) NOT NULL, \
        city CHAR(20) NOT NULL, \
        prepaid CHAR(30), \
        affiliation_number CHAR(20), \
        nickname CHAR(20));')
    connection.commit()

# Importar datos de archivo .csv

def import_residents_csv():
    with open('residents.csv') as fin:
        dr = csv.DictReader(fin)
        to_db = [(i['name'], i['last_name'], i['status'], i['admission_date'], i['birth_date'], i['age'], i['gender'], i['citizenship'], i['marital_status'], i['id_type'], 
            i['id_number'], i['address'], i['city'], i['prepaid'], i['affiliation_number'], i['nickname']) for i in dr]
        
        cursor.executemany('INSERT INTO residents(\
            name, \
            last_name, \
            status, \
            admission_date, \
            birth_date, \
            age, \
            gender, \
            citizenship,\
            marital_status, \
            id_type, \
            id_number, \
            address, \
            city, \
            prepaid, \
            affiliation_number, \
            nickname) \
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);', to_db)

# create_residents_table()
# import_residents_csv()
    
connection.commit()
connection.close()