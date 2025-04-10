import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def verify_database_connection():
    try:
        # Get database credentials from environment variables
        db_config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME')
        }
        
        # Try to connect to the database
        connection = mysql.connector.connect(**db_config)
        
        if connection.is_connected():
            print("Successfully connected to the database!")
            
            # Create cursor
            cursor = connection.cursor()
            
            # Verify database exists
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            
            if 'medical_tracking' not in databases:
                print("Creating medical_tracking database...")
                cursor.execute("CREATE DATABASE medical_tracking")
                print("Database created successfully!")
            
            # Switch to medical_tracking database
            cursor.execute("USE medical_tracking")
            
            # Verify user permissions
            cursor.execute("SHOW GRANTS FOR %s@%s", (os.getenv('DB_USER'), 'localhost'))
            grants = cursor.fetchall()
            print("\nCurrent user permissions:")
            for grant in grants:
                print(grant[0])
            
            cursor.close()
            connection.close()
            print("\nDatabase verification completed successfully!")
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        if err.errno == 1045:  # Access denied error
            print("\nAccess denied. Please check your username and password.")
            print("Try running the setup_database.sql script first.")
        elif err.errno == 2003:  # Can't connect to server
            print("\nCan't connect to MySQL server. Make sure MySQL is running.")
        elif err.errno == 1049:  # Unknown database
            print("\nDatabase doesn't exist. It will be created automatically.")

if __name__ == "__main__":
    verify_database_connection() 