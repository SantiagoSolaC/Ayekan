from threading import currentThread
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.src.models import (
    Resident,
    resident_instance_from_dictionary,
    resident_update_from_dictionary,
    resident_search_by_value,
    Medication,
    medication_search_by_value,
    medication_instance_from_dictionary,
    medication_update_from_dictionary,
)
from app.src.models import Prescription, prescription_search_by_value
from app import db
from . import views


@views.route("/")
def home():
    return render_template("home.html", active_item="home", user=current_user)


# Resident stuff


@views.route("/resident_search", methods=["GET", "POST"])
@login_required
def resident_search():
    if request.method == "GET":
        return render_template(
            "resident_search.html", active_item="resident", user=current_user
        )
    elif request.method == "POST":
        resident_list = resident_search_by_value(
            request.form.get("select_field"), request.form.get("imput_field")
        )
        for resident in resident_list:
            resident.to_show_in_html()
        return render_template(
            "resident_list.html",
            resident_list=resident_list,
            active_item="resident",
            user=current_user,
        )


@views.route("/resident_list", methods=["GET"])
@login_required
def resident_list():
    resident_list = Resident.query.all()
    for resident in resident_list:
        resident.to_show_in_html()
    return render_template(
        "resident_list.html",
        resident_list=resident_list,
        active_item="resident",
        user=current_user,
    )


@views.route("/resident_details/<int:id>", methods=["GET"])
@login_required
def resident_details(id):
    resident = Resident.query.get(int(id))
    resident.to_show_in_html()
    return render_template(
        "resident_details.html",
        resident=resident,
        active_item="resident",
        user=current_user,
    )


@views.route("/resident_new", methods=["GET", "POST"])
@login_required
def resident_new():
    if request.method == "GET":
        return render_template(
            "resident_new.html", active_item="resident", user=current_user
        )
    elif request.method == "POST":
        resident = resident_instance_from_dictionary(request.form)
        db.session.add(resident)
        db.session.commit()
        return redirect(url_for("views.resident_search"))


@views.route("/resident_details/<int:id>/edit", methods=["GET", "POST"])
@login_required
def resident_edit(id):
    if request.method == "GET":
        resident = Resident.query.get(int(id))
        resident.to_show_in_html()
        return render_template(
            "resident_edit.html",
            resident=resident,
            active_item="resident",
            user=current_user,
        )
    elif request.method == "POST":
        resident_update_from_dictionary(request.form)
        return redirect(url_for("views.resident_search"))


# Medication stuff


@views.route("/medication_search", methods=["GET", "POST"])
@login_required
def medication_search():
    if request.method == "GET":
        return render_template(
            "medication_search.html", active_item="medication", user=current_user
        )
    elif request.method == "POST":
        medication_list = medication_search_by_value(
            request.form.get("select_field"), request.form.get("imput_field")
        )
        for medication in medication_list:
            medication.to_show_in_html()
        return render_template(
            "medication_list.html",
            medication_list=medication_list,
            active_item="medication",
            user=current_user,
        )


@views.route("/medication_list", methods=["GET"])
@login_required
def medication_list():
    medication_list = Medication.query.all()
    return render_template(
        "medication_list.html",
        medication_list=medication_list,
        active_item="medication",
        user=current_user,
    )

@views.route("/medication_new", methods = ["GET", "POST"])
@login_required
def medication_new():
    if request.method == "GET":
        return render_template(
            "medication_new.html", active_item="medication", user=current_user
        )
    elif request.method == "POST":
        medication = medication_instance_from_dictionary(request.form)
        db.session.add(medication)
        db.session.commit()
        return redirect(url_for("views.medication_search"))

@views.route("/medication_details/<int:id>", methods = ["GET"])
@login_required
def medication_details(id):
    medication = Medication.query.get(int(id))
    medication.to_show_in_html()
    return render_template(
        "medication_details.html",
        medication = medication,
        active_item = "medication",
        user = current_user,
    )

@views.route("/medication_edit/<int:id>/edit", methods = ["GET", "POST"])
@login_required
def medication_edit(id):
    if request.method == "GET":
        medication = Medication.query.get(int(id))
        medication.to_show_in_html()
        return render_template(
            "medication_edit.html",
            medication = medication,
            active_item = "medication",
            user = current_user,
        )
    elif request.method == "POST":
        medication_update_from_dictionary(request.form)
        return redirect(url_for("views.medication_search"))
    

# Prescription stuff


@views.route("/prescription_search", methods=["GET", "POST"])
@login_required
def prescription_search():
    if request.method == "GET":
        return render_template(
            "prescription_search.html", active_item="prescription", user=current_user
        )
    elif request.method == "POST":
        prescription_list = prescription_search_by_value(
            request.form.get("select_field"), request.form.get("imput_field")
        )
        for prescription in prescription_list:
            prescription.to_show_in_html()
        return render_template(
            "prescription_list.html",
            prescription_list=prescription_list,
            active_item="prescription",
            user=current_user,
        )


@views.route("/prescription_list", methods=["GET"])
@login_required
def prescription_list():
    prescription_list = Prescription.query.all()
    return render_template(
        "prescription_list.html",
        prescription_list=prescription_list,
        active_item="prescription",
        user=current_user,
    )


@views.route("/prescription_new", methods=["GET", "POST"])
@login_required
def prescription_creation():
    if request.method == "GET":
        medication_list = Medication.query.all()
        medication_list
        return render_template(
            "prescription_new.html",
            active_item="prescription",
            user=current_user,
            medication_list=medication_list,
        )
    elif request.method == "POST":
        prescription = prescription_from_dictionary(request.form)
        print(prescription)
        db.session.add(prescription)
        db.session.commit()
        return redirect(url_for("views.prescription_list"))
