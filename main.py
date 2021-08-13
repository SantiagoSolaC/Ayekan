from flask import request, redirect, render_template
from app import create_app
from src.vademecum import get_medications_list, get_medication_by_id, edit_db_medication, create_new_medication, get_medication_list_by_value, edit_db_medication
from src.resident import get_residents_list, get_resident_by_id, edit_db_resident, get_resident_list_by_value
from src.prescription import get_prescriptions_list, get_prescription_by_id, edit_db_prescription
from src.stock import get_stock_from_value, get_stock_by_id, edit_db_stock, create_new_medication_stock
from src.substraction import substract_from_breakfast, substract_from_lunch, substract_from_tea, substract_from_dinner
from apscheduler.schedulers.background import BackgroundScheduler
import unittest
import atexit


app = create_app()


@app.before_first_request
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(substract_from_breakfast, "cron", hour="9")
    scheduler.add_job(substract_from_lunch, "cron", hour="12")
    scheduler.add_job(substract_from_tea, "cron", hour="17")
    scheduler.add_job(substract_from_dinner, "cron", hour="21")
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner().run(tests)


@app.route('/', methods = ["GET"])
def home():
    return render_template("home.html")


@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        pass
    elif request.method == "GET":
        return render_template("login.html")


@app.route("/new_resident", methods = ["GET", "POST"])
def new_resient():
    if request.method == "POST":
        return redirect("/new_resident")
    elif request.method == "GET":
        return render_template("/new_resident.html")


@app.route("/residents_list", methods = ["GET"])
def residents_list():
    residents_list = get_residents_list()
    for resident in residents_list:
        resident.to_show_in_html()
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


@app.route("/selected/<int:resident_id>", methods = ["GET"])
def selected(resident_id):
    resident = get_resident_by_id(resident_id)
    resident.to_show_in_html()
    return render_template("/resident_details.html", resident = resident)


@app.route("/edit_resident/<int:resident_id>", methods = ["GET"])
def edit_resident(resident_id):
    resident = get_resident_by_id(resident_id)
    resident.to_show_in_html()
    return render_template("/edit_resident.html", resident = resident)


@app.route("/edited_resident", methods = ["POST"])
def edited_resident():
    edit_db_resident(request.form)
    return redirect("/residents_list")


@app.route("/resident_search", methods = ["GET", "POST"])
def resident_search():
    if request.method == "GET":
        return render_template("/resident_search.html")
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


@app.route('/medications_list', methods = ['GET', 'POST'])
def medications_list():
    if request.method == 'GET':
        medications_list = get_medications_list()
        for medication in medications_list:
            medication.to_show_in_html()
        return render_template("/medications_list.html", medications_list = medications_list)
    elif request.method == 'POST':
        return redirect('/medication_new')


@app.route('/selected_medication/<int:medication_id>', methods = ['GET'])
def selected_medication(medication_id):
    medication = get_medication_by_id(medication_id)
    medication.to_show_in_html()
    return render_template('medication_details.html', medication = medication)


@app.route('/medication_edit/<int:medication_id>', methods = ['GET', 'POST'])
def medication_edit(medication_id):
    medication = get_medication_by_id(medication_id)
    medication.to_show_in_html()
    return render_template('medication_edit.html', medication = medication)


@app.route('/medication_update', methods = ['POST'])
def medication_update():
    edit_db_medication(request.form)
    return redirect('/medication_search')


@app.route('/medication_new', methods = ['GET', 'POST'])
def medication_new():
    if request.method == 'POST':
        create_new_medication(request.form)
        return redirect('/medications_list')
    elif request.method == 'GET':
        return render_template('/medication_new.html')


@app.route("/medication_search", methods = ["GET", "POST"])
def medication_search():
    if request.method == "GET":
        return render_template("/medication_search.html")
    elif request.method == "POST":
        select_field = request.form.get("select_field")
        imput_field = request.form.get("imput_field")
        medications_list = get_medication_list_by_value(select_field, imput_field)
        for medication in medications_list:
            medication.to_show_in_html()
        return render_template("/medications_list.html", medications_list = medications_list)



if __name__ == '__main__':
    app.run(port=5000)
