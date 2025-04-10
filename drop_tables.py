import os
import django
import MySQLdb

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical_tracking.settings')
django.setup()

from django.conf import settings

def drop_all_tables():
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
        
        # Get all tables
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        
        # Drop each table
        for table in tables:
            table_name = table[0]
            print(f"Dropping table: {table_name}")
            cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        
        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        
        db.commit()
        print("Successfully dropped all tables")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    drop_all_tables() 