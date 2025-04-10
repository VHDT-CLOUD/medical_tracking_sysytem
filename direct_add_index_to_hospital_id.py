import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical_tracking.settings')
django.setup()

from django.db import connection

def direct_add_index_to_hospital_id():
    with connection.cursor() as cursor:
        cursor.execute("ALTER TABLE accounts_hospital ADD INDEX hospital_id_idx (hospital_id);")
        print("Index added to hospital_id.")

if __name__ == "__main__":
    direct_add_index_to_hospital_id()
