import os
import django
import MySQLdb

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical_tracking.settings')
django.setup()

from django.conf import settings

def fix_database():
    try:
        # Connect to MySQL
        db = MySQLdb.connect(
            host=settings.DATABASES['default']['HOST'] or 'localhost',
            user=settings.DATABASES['default']['USER'],
            passwd=settings.DATABASES['default']['PASSWORD'],
            db=settings.DATABASES['default']['NAME']
        )
        
        cursor = db.cursor()
        
        # Disable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        
        # Drop all related tables
        cursor.execute("DROP TABLE IF EXISTS accounts_customuser;")
        cursor.execute("DROP TABLE IF EXISTS accounts_doctor;")
        cursor.execute("DROP TABLE IF EXISTS accounts_patient;")
        cursor.execute("DROP TABLE IF EXISTS accounts_medicalrecord;")
        cursor.execute("DROP TABLE IF EXISTS accounts_medicaldocument;")
        cursor.execute("DROP TABLE IF EXISTS accounts_profile;")
        cursor.execute("DROP TABLE IF EXISTS accounts_hospital;")
        
        # Create the hospital table with all required fields
        cursor.execute("""
            CREATE TABLE accounts_hospital (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(254) UNIQUE NOT NULL,
                address TEXT NOT NULL,
                registration_number VARCHAR(50) UNIQUE NOT NULL,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN NOT NULL DEFAULT TRUE,
                phone_number VARCHAR(15),
                website VARCHAR(200),
                description TEXT
            );
        """)
        
        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        
        db.commit()
        print("Successfully fixed hospital table structure")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    fix_database()