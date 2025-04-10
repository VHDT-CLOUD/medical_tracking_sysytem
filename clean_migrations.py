import os
import shutil

# Define the migrations to keep
migrations_to_keep = [
    '0001_initial.py',
    '0002_fix_hospital_field.py',
    '0004_alter_profile_aadhaar_number.py',
    '__init__.py',
    '_init_.py'  # This seems to be a typo but keeping it just in case
]

# Path to migrations directory
migrations_dir = os.path.join('accounts', 'migrations')

# Get all files in the migrations directory
all_files = os.listdir(migrations_dir)

# Create a backup directory
backup_dir = os.path.join('accounts', 'migrations_backup')
os.makedirs(backup_dir, exist_ok=True)

# Move files that are not in the keep list to the backup directory
for file in all_files:
    if file not in migrations_to_keep and not file.startswith('__pycache__'):
        src_path = os.path.join(migrations_dir, file)
        dst_path = os.path.join(backup_dir, file)
        
        # Check if it's a file (not a directory)
        if os.path.isfile(src_path):
            print(f"Moving {file} to backup directory")
            shutil.copy2(src_path, dst_path)
            os.remove(src_path)

print("Migration cleanup completed")