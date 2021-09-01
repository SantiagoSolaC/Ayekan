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
    Prescription,
    prescription_instance_from_dictionary,
    prescription_search_by_value,
    prescription_update_from_dictionary,
    medication_prescription
)
from app import db
from . import views


@views.route("/")
def home():
    return render_template("home.html", active_item="home", user=current_user)


# Resident stuff


resident_context = {"active_item": "resident",
                    "user": current_user}


@views.route("/resident_search", methods=["GET", "POST"])
@login_required
def resident_search():
    if request.method == "GET":
        return render_template(
            "resident_search.html", **resident_context
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
            **resident_context
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
        **resident_context
    )


@views.route("/resident_details/<int:id>", methods=["GET"])
@login_required
def resident_details(id):
    resident = Resident.query.get(int(id))
    resident.to_show_in_html()
    return render_template(
        "resident_details.html",
        resident=resident,
        **resident_context
    )


@views.route("/resident_new", methods=["GET", "POST"])
@login_required
def resident_new():
    if request.method == "GET":
        return render_template(
            "resident_new.html", **resident_context
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
            **resident_context
        )
    elif request.method == "POST":
        resident_update_from_dictionary(request.form)
        return redirect(url_for("views.resident_search"))


# Medication stuff


medication_context = {"active_item": "medication",
                      "user": current_user}


@views.route("/medication_search", methods=["GET", "POST"])
@login_required
def medication_search():
    if request.method == "GET":
        return render_template(
            "medication_search.html", **medication_context
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
            **medication_context
        )


@views.route("/medication_list", methods=["GET"])
@login_required
def medication_list():
    medication_list = Medication.query.all()
    return render_template(
        "medication_list.html",
        medication_list=medication_list,
        **medication_context
    )


@views.route("/medication_new", methods=["GET", "POST"])
@login_required
def medication_new():
    if request.method == "GET":
        return render_template(
            "medication_new.html", **medication_context
        )
    elif request.method == "POST":
        medication = medication_instance_from_dictionary(request.form)
        db.session.add(medication)
        db.session.commit()
        return redirect(url_for("views.medication_search"))


@views.route("/medication_details/<int:id>", methods=["GET"])
@login_required
def medication_details(id):
    medication = Medication.query.get(int(id))
    medication.to_show_in_html()
    return render_template("medication_details.html",
        medication=medication,
        **medication_context
    )


@views.route("/medication_edit/<int:id>/edit", methods=["GET", "POST"])
@login_required
def medication_edit(id):
    if request.method == "GET":
        medication = Medication.query.get(int(id))
        medication.to_show_in_html()
        return render_template(
            "medication_edit.html",
            medication=medication,
            **medication_context
        )
    elif request.method == "POST":
        medication_update_from_dictionary(request.form)
        return redirect(url_for("views.medication_search"))


# Prescription stuff


prescription_context = {"active_item": "prescription",
                        "user": current_user}


@views.route("/prescription_search", methods=["GET", "POST"])
@login_required
def prescription_search():
    if request.method == "GET":
        return render_template(
            "prescription_search.html", **prescription_context
        )
    elif request.method == "POST":
        if request.form.get("select_field") == "resident_name":
            resident_list = resident_search_by_value(
                "name", request.form.get("imput_field")
            )
            return render_template("/prescription_list_from_resident.html",
                                   resident_list=resident_list,
                                   **prescription_context
                                   )
        elif request.form.get("select_field") == "medication_name":
            medication_list = medication_search_by_value(
                "commercial_name", request.form.get("imput_field")
            )
            return render_template("prescription_list_from_medication.html",
                                   medication_list=medication_list,
                                   **prescription_context
                                   )


@views.route("/prescription_list/from_resident/<int:resident_id>", methods=["GET"])
@login_required
def prescription_list_from_resident(resident_id):
    resident = Resident.query.get(resident_id)
    prescription_list = resident.prescriptions
    # prescription_list = Resident.query.filter(
    #     Prescription.resident_id == resident_id).all()
    return render_template("prescription_list.html",
        prescription_list=prescription_list,
        **prescription_context
    )


@views.route("/prescription_list/from_medication/<int:medication_id>", methods=["GET"])
@login_required
def prescription_list_from_medication(medication_id):
    prescription_list = db.session.query(Prescription).join(
        medication_prescription).join(Medication).filter(Medication.id == medication_id).all()
    return render_template(
        "prescription_list.html",
        prescription_list=prescription_list,
        **prescription_context
    )


@views.route("/prescription_list", methods=["GET"])
@login_required
def prescription_list():
    prescription_list = Prescription.query.all()
    return render_template("prescription_list.html", prescription_list=prescription_list, **prescription_context)


@views.route("/prescription_details/<int:prescription_id>", methods = ["GET", "POST"])
@login_required
def prescription_details(prescription_id):
    prescription = Prescription.query.get(int(prescription_id))
    administration_route = prescription.medications[0].pharmaceutical_form
    # prescription.to_show_in_html()
    return render_template("prescription_details.html",
                            prescription = prescription,
                            administration_route = administration_route,
                            **prescription_context
                            )


@views.route("/prescription_details/<int:prescription_id>/edit", methods = ["GET", "POST"])
@login_required
def prescription_edit(prescription_id):
    if request.method == "GET":
        prescription = Prescription.query.get(int(prescription_id))
        # prescription.to_show_in_html()
        return render_template("prescription_edit.html",
                                prescription = prescription,
                                **prescription_context
                                )
    elif request.method == "POST":
        prescription_update_from_dictionary(request.form)
        
        return redirect(url_for("views.prescription_search"))


@views.route("/prescription_new", methods=["GET", "POST"])
@login_required
def prescription_new():
    if request.method == "GET":
        medication_list = Medication.query.all()
        resident_list = Resident.query.all()
        return render_template(
            "prescription_new.html",
            active_item="prescription",
            user=current_user,
            medication_list=medication_list,
            resident_list=resident_list
        )
    elif request.method == "POST":
        prescription = prescription_instance_from_dictionary(request.form) 
        medication = Medication.query.get(request.form.get("medication_id"))
        prescription.medications.append(medication)
        db.session.add(prescription)
        db.session.commit()
        return redirect(url_for("views.prescription_search"))
