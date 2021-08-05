from flask import request, redirect, render_template
from app import create_app
from src.medication import get_medications_list
from src.resident import get_residents_list, get_resident_by_id, edit_db_resident, get_resident_list_by_value
from src.prescription import get_prescriptions_list, get_prescription_by_id, edit_db_prescription
from src.stock import get_stock_from_value, get_stock_by_id, edit_db_stock, create_new_medication_stock
from src.substraction import substract_from_breakfast, substract_from_lunch, substract_from_tea, substract_from_dinner
from apscheduler.schedulers.background import BackgroundScheduler
import schedule
import unittest
import time


scheduler = BackgroundScheduler()


app = create_app()


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner().run(tests)


@app.route('/', methods = ["GET", "POST"])
def hello():
    return render_template("hello.html", res=None)


@app.route("/login", methods = ["POST"])
def login():
    dictionary = {"name": request.form["_email"]}
    return render_template("hello.html", res=dictionary)


@app.route("/new_resident", methods = ["GET", "POST"])
def new_resient():
    if request.method == "POST":
        return redirect("/new_resident")
    elif request.method == "GET":
        return render_template("/new_resident.html")


@app.route("/residents_list", methods = ["GET"])
def residents_list():
    residents_list = get_residents_list()
    return render_template('/residents_list.html', residents_list = residents_list)


@app.route("/prescriptions_list", methods = ["GET"])
def prescriptions_list():
    prescriptions_list = get_prescriptions_list()
    for prescription in prescriptions_list:
        prescription.to_show_in_html()
    return render_template('/prescriptions_list.html', prescriptions_list = prescriptions_list)


@app.route("/selected_prescription/<int:prescription_id>", methods = ["GET", "POST"])
def selected_prescription(prescription_id):
    if request.method == "GET":
        medications_list = get_medications_list()
        for medication in medications_list:
            medication.to_show_in_html()
        prescription = get_prescription_by_id(prescription_id)
        resident = get_resident_by_id(prescription.resident_id)
        prescription.to_show_in_html()
        resident.to_show_in_html()
        days_left = prescription.days_left()
        return render_template("/edit_prescription.html", prescription = prescription, days_left = days_left, medications_list = medications_list, resident = resident)
    elif request.method == "POST":
        edit_db_prescription(request.form)
        return redirect("/prescriptions_list")
    
    
@app.route("/edited_prescription", methods = ["POST"])
def edited_prescription():
    edit_db_prescription(request.form)
    return redirect("/prescriptions_list")


@app.route("/new_stock/<int:prescription_id>", methods = ["GET"])
def new_stock(prescription_id):
    prescription = get_prescription_by_id(prescription_id)
    medications_list = get_medications_list()
    for medication in medications_list:
        medication.to_show_in_html()
    return render_template("new_stock.html", prescription = prescription, medications_list = medications_list)
    

@app.route("/new_medication_stock", methods = ["POST"])
def new_medication_stock():
    stock_dictionary = request.form
    prescription_id = stock_dictionary.get("prescription_id")
    create_new_medication_stock(stock_dictionary)
    return redirect(f"/stock_list/{prescription_id}")


@app.route("/stock_list/<int:prescription_id>", methods = ["GET"])
def stock_list(prescription_id):
    stock_list = get_stock_from_value("prescription_id", prescription_id)
    for stock in stock_list:
        stock.to_show_in_html()
    return render_template("/stock_list.html", stock_list = stock_list, prescription_id = prescription_id)


@app.route("/stock_details/<int:stock_id>", methods = ["GET"])
def stock_details(stock_id):
    stock = get_stock_by_id(stock_id)
    medications_list = get_medications_list()
    for medication in medications_list:
        medication.to_show_in_html()
    stock.to_show_in_html()
    return render_template("/stock_details.html", stock = stock, medications_list = medications_list)


@app.route("/adjust_stock", methods = ["POST"])
def adjust_stock():
    stock_dictionary = request.form
    prescription_id = stock_dictionary.get('prescription_id')
    edit_db_stock(request.form)
    return redirect(f"/stock_list/{prescription_id}")


@app.route("/selected/<int:id>", methods = ["GET"])
def selected(resident_id):
    resident = get_resident_by_id(resident_id)
    resident.to_show_in_html()
    return render_template("/resident_details.html", resident = resident)


@app.route("/edit_resident/<int:id>", methods = ["GET"])
def edit_resident(resident_id):
    resident = get_resident_by_id(resident_id)
    return render_template("/edit_resident.html", resident = resident)


@app.route("/edited_resident", methods = ["POST"])
def edited_resident():
    edit_db_resident(request.form)
    return redirect("/residents_list")


@app.route("/search", methods = ["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("/search.html")
    elif request.method == "POST":
        select_field = request.form.get("select_field")
        imput_field = request.form.get("imput_field")
        residents_list = get_resident_list_by_value(select_field, imput_field)
        for resident in residents_list:
            resident.to_show_in_html()
        return render_template("/residents_list.html", residents_list = residents_list)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html', error=error)


def job():
    print("sarasa")
    

schedule.every(3).seconds.do(job)
schedule.every().day.at("13:56").do(substract_from_breakfast)
schedule.every().day.at("12:00").do(substract_from_lunch)
schedule.every().day.at("17:00").do(substract_from_tea)
schedule.every().day.at("21:00").do(substract_from_dinner)

schedule.run_pending()


if __name__ == '__main__':
    app.run(port=5000)
