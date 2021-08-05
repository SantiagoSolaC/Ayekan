import sqlite3
from src.new_resident import get_residents_list

def residents_table_to_lower():
    with sqlite3.connect("./ayekan.db") as conn:
        cursor = conn.cursor()
        residents_list = get_residents_list()
        for resident in residents_list:
            cursor.execute(f'UPDATE residents SET \
            name="{resident.name.lower()}", \
            last_name="{resident.last_name.lower()}", \
            status="{resident.status.lower()}", \
            admission_date="{resident.admission_date}", \
            birth_date="{resident.birth_date}", \
            age="{resident.age}", \
            gender="{resident.gender.lower()}", \
            citizenship="{resident.citizenship.lower()}", \
            marital_status="{resident.marital_status.lower()}", \
            id_type="{resident.id_type.lower()}", \
            id_number="{resident.id_number}", \
            address="{resident.address.lower()}", \
            city="{resident.city.lower()}", \
            prepaid="{resident.prepaid.lower()}", \
            affiliation_number="{resident.affiliation_number}", \
            nickname="{resident.nickname.lower()}" \
            WHERE id={resident.id};')

