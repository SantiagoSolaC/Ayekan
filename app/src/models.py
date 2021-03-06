from app import db
from datetime import datetime


# Resident table creation with his functions..

class Resident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False)
    admission_date = db.Column(db.String(10), nullable=False)
    nickname = db.Column(db.String(50))
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    citizenship = db.Column(db.String(50))
    marital_status = db.Column(db.String(50))
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    id_type = db.Column(db.String(50), nullable=False)
    id_number = db.Column(db.String(50), nullable=False, unique=True)
    prepaid = db.Column(db.String(100))
    affiliation_number = db.Column(db.String(100))

    stocks = db.relationship("Stock", backref="resident")
    prescriptions = db.relationship("Prescription", backref="resident")

    def to_show_in_html(self):
        self.status = self.status.title()
        self.nickname = self.nickname.upper()
        self.name = self.name.title()
        self.last_name = self.last_name.title()
        self.gender = self.gender.title()
        self.citizenship = self.citizenship.title()
        self.marital_status = self.marital_status.title()
        self.address = self.address.title()
        self.city = self.city.title()
        self.id_type = self.id_type.upper()
        self.prepaid = self.prepaid.upper()

    def to_store_in_db(self):
        self.status = self.status.lower()
        self.nickname = self.nickname.lower()
        self.name = self.name.lower()
        self.last_name = self.last_name.lower()
        self.gender = self.gender.lower()
        self.citizenship = self.citizenship.lower()
        self.marital_status = self.marital_status.lower()
        self.address = self.address.lower()
        self.city = self.city.lower()
        self.id_type = self.id_type.lower()
        self.prepaid = self.prepaid.lower()


def resident_search(value):
    resident = Resident.query.filter_by(name == value).first()
    print(resident)
    resident_id = resident.id
    print(resident_id)
    return resident_id


def resident_search_by_value(select_field, imput_field):
    if select_field == "status":
        if imput_field != "":
            resident_list = Resident.query.filter(
                Resident.status.like(imput_field)
            ).all()
            return resident_list
        else:
            resident_list = Resident.query.all()
            return resident_list
    elif select_field == "nickname":
        resident_list = Resident.query.filter(Resident.nickname.like(imput_field)).all()
        return resident_list
    elif select_field == "name":
        resident_list = Resident.query.filter(Resident.name.like(imput_field)).all()
        return resident_list
    elif select_field == "last_name":
        resident_list = Resident.query.filter(
            Resident.last_name.like(imput_field)
        ).all()
        return resident_list


def resident_instance_from_dictionary(resident_dictionary):
    new_resident = Resident(
        status=resident_dictionary.get("status"),
        admission_date=resident_dictionary.get("admission_date"),
        nickname=resident_dictionary.get("nickname"),
        name=resident_dictionary.get("name"),
        last_name=resident_dictionary.get("last_name"),
        birth_date=resident_dictionary.get("birth_date"),
        age=resident_dictionary.get("age"),
        gender=resident_dictionary.get("gender"),
        citizenship=resident_dictionary.get("citizenship"),
        marital_status=resident_dictionary.get("marital_status"),
        address=resident_dictionary.get("address"),
        city=resident_dictionary.get("city"),
        id_type=resident_dictionary.get("id_type"),
        id_number=resident_dictionary.get("id_number"),
        prepaid=resident_dictionary.get("prepaid"),
        affiliation_number=resident_dictionary.get("affiliation_number"),
    )
    new_resident.to_store_in_db()
    return new_resident


def resident_update_from_dictionary(request_form):
    db.session.query(Resident).filter_by(id=request_form.get("id")).update(request_form)
    db.session.commit()


# medication_presciption table creation (relationship betwen medication and prescription tables)..

medication_prescription = db.Table(
    "medication_prescription",
    db.Column(
        "medication_id", db.Integer, db.ForeignKey("medication.id"), primary_key=True
    ),
    db.Column(
        "prescription_id",
        db.Integer,
        db.ForeignKey("prescription.id"),
        primary_key=True,
    ),
)


# Medication table creation with his functions..

class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drug_name = db.Column(db.String(100), nullable=False)
    commercial_name = db.Column(db.String(100), nullable=False, unique=True)
    pharmaceutical_form = db.Column(db.String(50), nullable=False)
    measurement_unit = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float)
    stocks = db.relationship("Stock", backref="medication")
    # prescriptions = db.relationship("Prescription", secondary=medication_prescription)

    def to_show_in_html(self):
        self.drug_name.title()
        self.commercial_name.title()
        self.pharmaceutical_form.title()

    def to_store_in_db(self):
        self.drug_name.lower()
        self.commercial_name.lower()
        self.pharmaceutical_form.lower()

    stocks = db.relationship("Stock", backref="medication")


def medication_instance_from_dictionary(medication_dictionary):
    new_medication = Medication(
        drug_name = medication_dictionary.get("drug_name"),
        commercial_name = medication_dictionary.get("commercial_name"),
        pharmaceutical_form = medication_dictionary.get("pharmaceutical_form"),
        measurement_unit = medication_dictionary.get("measurement_unit"),
        amount = medication_dictionary.get("amount")
    )
    new_medication.to_store_in_db()
    return new_medication


def medication_search_by_value(select_field, imput_field):
    if select_field == "commercial_name":
        if imput_field != "":
            medication_list = Medication.query.filter(
                Medication.commercial_name.like(imput_field)
            ).all()
            return medication_list
        else:
            medication_list = Medication.query.all()
            return medication_list
    elif select_field == "drug_name":
        medication_list = Medication.query.filter(
            Medication.drug_name.like(imput_field)
        ).all()
        return medication_list


def medication_update_from_dictionary(request_form):
    db.session.query(Medication).filter_by(id=request_form.get("id")).update(request_form)
    db.session.commit()


# Stock table creation..

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.Integer, db.ForeignKey("resident.id"), nullable=False)
    medication_id = db.Column(
        db.Integer, db.ForeignKey("medication.id"), nullable=False
    )
    prescription_id = db.Column(
        db.Integer, db.ForeignKey("prescription.id"), nullable=False
    )
    amount = amount = db.Column(db.Float)
    notes = db.Column(db.String(200))
    date = db.Column(db.Date, nullable=False)


# Prescription table creation with gist functions..

class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.Integer, db.ForeignKey("resident.id"), nullable=False)
    # medication_id = db.Column(db.Integer, db.ForeignKey('medication.id'), nullable = False)
    medications = db.relationship("Medication", secondary=medication_prescription)
    administration_route = db.Column(db.String(100), nullable=False)
    breakfast = db.Column(db.Integer)
    lunch = db.Column(db.Integer)
    tea = db.Column(db.Integer)
    dinner = db.Column(db.Integer)
    notes = db.Column(db.String(200))
    medication_status = db.Column(db.String(100))
    prescription_date = db.Column(db.String(20), nullable=False)
    last_registry_date = db.Column(db.String(20))
    in_pillbox = db.Column(db.String(50), nullable=False)
    floor = db.Column(db.String(50), nullable=False)

    stocks = db.relationship("Stock", backref="prescription")

    def to_show_in_html(self):
        self.resident_id = self.resident_id.nickname.upper()
        self.medication_id = self.medication_id.commercial_name.title()
        self.administration_route.title()
        self.medication_status.title()
        self.in_pillbox.upper()
        self.floor.upper()

    def to_store_in_db(self):
        self.administration_route.lower()
        self.in_pillbox.lower()
        self.floor.lower()


def prescription_search_by_value(select_field, imput_field):
    if select_field == "resident_id":
        if imput_field != "":
            resident_id = resident_search(imput_field)
            prescription_list = Prescription.query.filter(
                Prescription.resident_id.like(resident_id)
            ).all()
            return prescription_list
        else:
            prescription_list = Prescription.query.all()
            return prescription_list
    elif select_field == "medication_id":
        prescription_list = Prescription.query.filter(
            Prescription.medication_id.like(imput_field)
        ).all()
        return prescription_list


def prescription_from_dictionary(prescription_dictionary):
    new_prescription = Prescription(
        resident_id=prescription_dictionary.get("resident_id"),
        # medications = prescription_dictionary.get("medication_id"),
        administration_route=prescription_dictionary.get("administration_route"),
        breakfast=prescription_dictionary.get("breakfast"),
        lunch=prescription_dictionary.get("lunch"),
        tea=prescription_dictionary.get("tea"),
        dinner=prescription_dictionary.get("dinner"),
        notes=prescription_dictionary.get("notes"),
        medication_status=prescription_dictionary.get("medication_status"),
        prescription_date=prescription_dictionary.get("prescription_date"),
        last_registry_date=prescription_dictionary.get("last_registry_date"),
        in_pillbox=prescription_dictionary.get("in_pillbox"),
        floor=prescription_dictionary.get("floor"),
    )
    # new_prescription.to_store_in_db()
    return new_prescription
