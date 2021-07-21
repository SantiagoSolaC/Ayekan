import csv, sqlite3
connection = sqlite3.connect('ayekan.db')
cursor = connection.cursor()

# Crear tabla 'stock_registry' con todas las columnas.

def create_stock_registry_table():
    cursor.execute('CREATE TABLE IF NOT EXISTS stock_registry(\
        id INTEGER PRIMARY KEY AUTOINCREMENT, \
        resident_id CHAR(50) NOT NULL, \
        medication_id CHAR(100) NOT NULL, \
        amount INT(10), \
        notes CHAR(200), \
        date DATE);')
    connection.commit()

# Importar datos de archivo .csv

def import_stock_registry_csv():
    with open('stock_registry.csv') as fin:
        dr = csv.DictReader(fin)
        to_db = [(i['resident_id'], i['medication_id'], i['amount'], i['notes'], i['date']) for i in dr]
        
        cursor.executemany('INSERT INTO stock_registry(\
            resident_id, \
            medication_id, \
            amount, \
            notes, \
            date) \
            VALUES (?,?,?,?,?);', to_db)

# create_stock_registry_table()
# import_stock_registry_csv()

connection.commit()
connection.close()