import csv, sqlite3
connection = sqlite3.connect('ayekan.db')
cursor = connection.cursor()

# Crear tabla 'prescriptions' con todas las columnas.

def create_prescriptions_table():
    cursor.execute('CREATE TABLE IF NOT EXISTS prescriptions(\
        id INTEGER PRIMARY KEY AUTOINCREMENT, \
        resident_id CHAR(50) NOT NULL, \
        medication_id CHAR(100) NOT NULL, \
        administration_route CHAR(20) NOT NULL, \
        breakfast FLOAT(4), \
        lunch FLOAT(4), \
        tea FLOAT(4), \
        dinner FLOAT(4), \
        total_per_day FLOAT(4), \
        stock FLOAT(4), \
        days_left FLOAT(4), \
        notes CHAR(200), \
        medication_status CHAR(20) NOT NULL, \
        prescription_date DATE, \
        last_registry_date DATE, \
        in_pillbox BOOL NOT NULL, \
        floor CHAR(4) NOT NULL, \
        resident_status CHAR(20) NOT NULL);')
    connection.commit()

# Importar datos de archivo .csv

def import_prescriptions_csv():
    with open('prescriptions.csv') as fin:
        dr = csv.DictReader(fin)
        to_db = [(i['resident_id'], i['medication_id'], i['administration_route'], i['breakfast'], i['lunch'], i['tea'], i['dinner'], i['total_per_day'],
                 i['stock'], i['days_left'], i['notes'], i['medication_status'], i['prescription_date'], i['last_registry_date'], i['in_pillbox'], i['floor'], i['resident_status']) 
                 for i in dr]
        
        cursor.executemany('INSERT INTO prescriptions(\
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
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);', to_db)

# create_prescriptions_table()
# import_prescriptions_csv()

connection.commit()
connection.close()