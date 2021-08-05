import csv, sqlite3
connection = sqlite3.connect('ayekan.db')
cursor = connection.cursor()

# Crear tabla 'prescriptions_registry' con todas las columnas.

def create_prescriptions_registry_table():
    cursor.execute('CREATE TABLE IF NOT EXISTS prescriptions_registry(\
        id INTEGER PRIMARY KEY AUTOINCREMENT, \
        resident_id CHAR(50) NOT NULL, \
        medication_id CHAR(100) NOT NULL, \
        commercial_name CHAR(100) NOT NULL, \
        administration_route CHAR(20) NOT NULL, \
        breakfast FLOAT(4), \
        lunch FLOAT(4), \
        tea FLOAT(4), \
        dinner FLOAT(4), \
        notes CHAR(200), \
        medication_status CHAR(20) NOT NULL, \
        prescription_date DATE, \
        last_registry_date DATE, \
        in_pillbox BOOL NOT NULL, \
        floor CHAR(4) NOT NULL, \
        resident_status CHAR(20) NOT NULL);')
    connection.commit()

# Importar datos de archivo .csv

def import_prescriptions_registry_csv():
    with open('prescriptions_registry.csv') as fin:
        dr = csv.DictReader(fin)
        to_db = [(i['resident_id'], i['medication_id'], i['commercial_name'], i['administration_route'], i['breakfast'], i['lunch'], i['tea'], i['dinner'], i['notes'], 
            i['medication_status'], i['prescription_date'], i['last_registry_date'], i['in_pillbox'], i['floor'], i['resident_status']) for i in dr]
        
        cursor.executemany('INSERT INTO prescriptions_registry(\
            resident_id, \
            medication_id, \
            commercial_name, \
            administration_route, \
            breakfast, \
            lunch, \
            tea, \
            dinner, \
            notes, \
            medication_status, \
            prescription_date, \
            last_registry_date, \
            in_pillbox, \
            floor, \
            resident_status) \
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);', to_db)

# create_prescriptions_registry_table()
# import_prescriptions_registry_csv()

connection.commit()
connection.close()