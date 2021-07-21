from new_prescription import Prescription, edit_prescription
import sqlite3
connection = sqlite3.connect('ayekan.db')
cursor = connection.cursor()

# Crear clase 'StockRegistry'.

class StockRegistry:
    def __init__(self, stock_registry_tuple):
        self.id = stock_registry_tuple[0]
        self.resident_id = stock_registry_tuple[1]
        self.medication_id = stock_registry_tuple[2]
        self.amount = stock_registry_tuple[3]
        self.notes = stock_registry_tuple[4]
        self.date = stock_registry_tuple[5]


# Crear un nuevo registro en la tabla 'stock_registry'.

def insert_new_stock_registry(stock_registry_tuple):
    stock_registry = StockRegistry(stock_registry_tuple)
    cursor.execute(f'INSERT INTO stock_registry(\
        resident_id, \
        medication_id, \
        amount, \
        notes, \
        date) \
        VALUES ("{stock_registry.resident_id}", "{stock_registry.medication_id}", "{stock_registry.amount}", "{stock_registry.notes}", "{stock_registry.date}");')
    connection.commit()
    
# Actualizar el stock, días restantes y fecha de registro de la tabla 'prescriptions'. Crea un nuevo registro en 'stock_registry'.

def update_prescriptions_stock(stock_registry_tuple):
    insert_new_stock_registry(stock_registry_tuple)
    stock_registry = StockRegistry(stock_registry_tuple)
    cursor.execute(f'SELECT * \
                    FROM prescriptions \
                    WHERE resident_id="{stock_registry.resident_id}" \
                    AND medication_id="{stock_registry.medication_id}";')
    prescription_tuple = cursor.fetchone()
    if prescription_tuple != None:
        prescription = Prescription(prescription_tuple)
        updated_stock = prescription.stock + stock_registry.amount
        days_left = updated_stock / prescription.total_per_day
        updated_stock_tuple = (prescription.id, prescription.resident_id, prescription.medication_id, prescription.administration_route, prescription.breakfast, prescription.lunch,
            prescription.tea, prescription.dinner, prescription.total_per_day, updated_stock, days_left, prescription.notes, prescription.medication_status, prescription.prescription_date, 
            stock_registry.date, prescription.in_pillbox, prescription.floor, prescription.resident_status)
        edit_prescription(updated_stock_tuple)

connection.close()