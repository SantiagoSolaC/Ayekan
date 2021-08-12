import csv, sqlite3
connection = sqlite3.connect('ayekan.db')
cursor = connection.cursor()

# Crear tabla 'vademecum' con todas las columnas.

def create_vademecum_table():
    cursor.execute('CREATE TABLE IF NOT EXISTS vademecum(\
        medication_id INTEGER PRIMARY KEY AUTOINCREMENT, \
        drug_name TEXT NOT NULL, \
        commercial_name TEXT NOT NULL, \
        pharmaceutical_form TEXT NOT NULL, \
        measurement_unit TEXT NOT NULL, \
        amount REAL NOT NULL);')
    connection.commit()

# Importar datos de archivo .csv

def import_vademecum_csv():
    with open('vademecum.csv') as fin:
        dr = csv.DictReader(fin)
        to_db = [(i['drug_name'], i['commercial_name'], i['pharmaceutical_form'], i['measurement_unit'], i['amount']) for i in dr]
        
        cursor.executemany('INSERT INTO vademecum(\
            drug_name, \
            commercial_name, \
            pharmaceutical_form, \
            measurement_unit, \
            amount) \
            VALUES (?,?,?,?,?);', to_db)
        
# create_vademecum_table()
# import_vademecum_csv()
    
connection.commit()
connection.close()