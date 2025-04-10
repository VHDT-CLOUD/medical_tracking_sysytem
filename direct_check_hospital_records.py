import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical_tracking.settings')
django.setup()

from django.db import connection

def direct_check_hospital_records():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM accounts_hospital;")
        records = cursor.fetchall()
        if not records:
            print("No records found in accounts_hospital.")
        else:
            for record in records:
                print(record)

if __name__ == "__main__":
    direct_check_hospital_records()
