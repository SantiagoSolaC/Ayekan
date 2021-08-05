import sqlite3
import time
from src.resident import get_resident_by_id, get_resident_by_value
from src.medication import get_medication_by_id, get_medication_by_value

# Crear clase 'Stock'.


class Stock:
    def __init__(self, stock_dictionary):
        self.stock_id = stock_dictionary.get('stock_id')
        self.resident_id = stock_dictionary.get('resident_id')
        self.medication_id = stock_dictionary.get('medication_id')
        self.amount = stock_dictionary.get('amount')
        self.notes = stock_dictionary.get('notes')
        self.date = stock_dictionary.get('date')
        self.prescription_id = stock_dictionary.get('prescription_id')

    def to_show_in_html(self):
        self.resident_id = get_resident_by_id(self.resident_id).nickname.upper()
        self.medication_id = get_medication_by_id(self.medication_id).commercial_name.title()

    def to_store_in_db(self):
        if not self.resident_id.isnumeric():
            self.resident_id =  get_resident_by_value("nickname", self.resident_id).id
        if not self.medication_id.isnumeric():
            self.medication_id = get_medication_by_value("commercial_name", self.medication_id).id

    def choose_next_medication(self):
        with sqlite3.connect("./ayekan.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM stock WHERE prescription_id = "{self.prescription_id}" AND amount > "0";')
            result = cursor.fetchone()
            stock_dictionary = create_stock_dictionary(result)
            stock = Stock(stock_dictionary)

# Crear diccionario 'stock' desde tupla.


def create_stock_dictionary(stock_tuple):
    stock_dictionary = {
        "stock_id": stock_tuple[0],
        "resident_id": stock_tuple[1],
        "medication_id": stock_tuple[2],
        "amount": stock_tuple[3],
        "notes": stock_tuple[4],
        "date": stock_tuple[5],
        "prescription_id": stock_tuple[6]
    }
    return stock_dictionary

# Crear un nuevo registro en las tablas 'stock' y 'stock_registry'. Recibe un diccionario.


def create_new_medication_stock(stock_dictionary):
    stock = Stock(stock_dictionary)
    stock.to_store_in_db()
    with sqlite3.connect("./ayekan.db") as conn:
        cursor = conn.cursor()
        cursor.executescript(f'INSERT INTO stock (resident_id, medication_id, amount, notes, date, prescription_id) VALUES ("{stock.resident_id}", "{stock.medication_id}", \
        "{stock.amount}", "{stock.notes}", "{time.strftime("%Y-%m-%d")}", "{stock.prescription_id}"); \
        INSERT INTO stock_registry (type, stock_id, resident_id, medication_id, amount, notes, date, prescription_id, registry_date) VALUES ("creation", "{stock.stock_id}", \
        "{stock.resident_id}", "{stock.medication_id}", "{stock.amount}", "{stock.notes}", "{time.strftime("%Y-%m-%d")}", "{stock.prescription_id}", \
        "{time.strftime("%Y-%m-%d")}");')
        
# Editar un registro de la tabla a partir de su ID. Crea entrada en la tabla 'stock_registry'. Recibe un diccionario.


def edit_db_stock(stock_dictionary):
    stock = Stock(stock_dictionary)
    stock.to_store_in_db()
    with sqlite3.connect("./ayekan.db") as conn:
        cursor = conn.cursor()
        cursor.executescript(f'UPDATE stock SET resident_id = "{stock.resident_id}", medication_id = "{stock.medication_id}", amount = "{stock.amount}", \
        notes = "{stock.notes}", date = "{stock.date}", prescription_id = "{stock.prescription_id}" WHERE stock_id = "{stock.stock_id}"; \
        INSERT INTO stock_registry (type, stock_id, resident_id, medication_id, amount, notes, date, prescription_id, registry_date) VALUES ("modification", \
        "{stock.stock_id}", "{stock.resident_id}", "{stock.medication_id}", "{stock.amount}", "{stock.notes}", "{stock.date}", "{stock.prescription_id}", \
        "{time.strftime("%Y-%m-%d")}");')

# Ver una lista de stock a partir de un valor. Devuelve una lista de instancias.


def get_stock_from_value(field_name, value):
    with sqlite3.connect("./ayekan.db") as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM stock WHERE {field_name} = "{value}";')
        stock_list = []
        result = cursor.fetchall()
        for stock_tuple in result:
            stock_dictionary = create_stock_dictionary(stock_tuple)
            stock = Stock(stock_dictionary)
            stock_list.append(stock)
        return stock_list        

# Buscar stock por número de ID. Devuelve instancia.


def get_stock_by_id(stock_id):
    with sqlite3.connect("./ayekan.db") as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM stock WHERE stock_id = "{stock_id}";')
        result = cursor.fetchone()
        stock_dictionary = create_stock_dictionary(result)
        stock = Stock(stock_dictionary)
        return stock

# Ver una lista de stock.


def get_stock_list():
    with sqlite3.connect("./ayekan.db") as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM stock;')
        stock_list = []
        result = cursor.fetchall()
        for stock_tuple in result:
            stock_dictionary = create_stock_dictionary(stock_tuple)
            stock = Stock(stock_dictionary)
            stock_list.append(stock)
        return stock_list
