import os
import subprocess

print("=== Fixing conflicting migrations ===")

# Step 1: Create a merge migration
print("\n=== Step 1: Creating a merge migration ===")
try:
    result = subprocess.run(
        ['python', 'manage.py', 'makemigrations', '--merge', '--no-input'],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print("Errors:")
        print(result.stderr)
except Exception as e:
    print(f"Error creating merge migration: {e}")

# Step 2: Apply the migrations
print("\n=== Step 2: Applying migrations ===")
try:
    result = subprocess.run(
        ['python', 'manage.py', 'migrate'],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print("Errors:")
        print(result.stderr)
except Exception as e:
    print(f"Error applying migrations: {e}")

print("\n=== Migration fix completed ===")
print("Please test your application now to ensure everything is working correctly.")