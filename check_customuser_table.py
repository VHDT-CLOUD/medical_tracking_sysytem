import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical_tracking.settings')
django.setup()

from django.db import connection

def check_customuser_table():
    with connection.cursor() as cursor:
        cursor.execute("SHOW COLUMNS FROM accounts_customuser;")
        columns = cursor.fetchall()
        for column in columns:
            print(column)

if __name__ == "__main__":
    check_customuser_table()
