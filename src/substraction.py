import sqlite3

# Crear clase 'substraction' a partir de una tupla (no se va a mostrar en html).


class Substraction:
    
    def __init__(self, substraction_tuple):
        self.stock_id = substraction_tuple[0]
        self.prescription_id = substraction_tuple[1]
        self.breakfast = substraction_tuple[2]
        self.lunch = substraction_tuple[3]
        self.tea = substraction_tuple[4]
        self.dinner = substraction_tuple[5]
        self.amount = substraction_tuple[6]

# Listar stock para restar diariamente.


def get_stock_substraction_list():
    with sqlite3.connect("./ayekan.db") as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT stock.stock_id, prescriptions.prescription_id, breakfast, lunch, tea, dinner, stock.amount FROM prescriptions INNER JOIN stock \
        ON prescriptions.prescription_id = stock.prescription_id;')
        result = cursor.fetchall()
        stock_substraction_list = []
        for stock_substraction in result:
            stock = Substraction(stock_substraction)
            if stock.amount > 0:
                stock_substraction_list.append(stock)
        return stock_substraction_list

# Restar stock por horario.


def substract_from_breakfast():
    stock_substraction_list = get_stock_substraction_list()
    print('breakfasted')
    with sqlite3.connect("./ayekan.db") as conn:
        cursor = conn.cursor()
        for stock in stock_substraction_list:
            if stock.breakfast > 0:
                stock.amount -= stock.breakfast
                cursor.execute(f'UPDATE stock SET amount = "{stock.amount}" WHERE stock_id = "{stock.stock_id}";')
    print('breakfasted')
    

def substract_from_lunch():
    stock_substraction_list = get_stock_substraction_list()
    with sqlite3.connect("./ayekan.db") as conn:
        cursor = conn.cursor()
        for stock in stock_substraction_list:
            if stock.lunch > 0:
                stock.amount -= stock.lunch
                cursor.execute(f'UPDATE stock SET amount = "{stock.amount}" WHERE stock_id = "{stock.stock_id}";')
                

def substract_from_tea():
    stock_substraction_list = get_stock_substraction_list()
    with sqlite3.connect("./ayekan.db") as conn:
        cursor = conn.cursor()
        for stock in stock_substraction_list:
            if stock.tea > 0:
                stock.amount -= stock.tea
                cursor.execute(f'UPDATE stock SET amount = "{stock.amount}" WHERE stock_id = "{stock.stock_id}";')


def substract_from_dinner():
    stock_substraction_list = get_stock_substraction_list()
    with sqlite3.connect("./ayekan.db") as conn:
        cursor = conn.cursor()
        for stock in stock_substraction_list:
            if stock.dinner > 0:
                stock.amount -= stock.dinner
                cursor.execute(f'UPDATE stock SET amount = "{stock.amount}" WHERE stock_id = "{stock.stock_id}";')
