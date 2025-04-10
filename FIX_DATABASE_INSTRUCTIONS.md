# Database Fix Instructions

This document provides instructions to fix the issue with the missing `hospital_id` column in the `accounts_customuser` table and resolve conflicting migrations.

## Issue Description

The error indicates that there are conflicting migrations in the accounts app, and the `hospital_id` column might be missing in the `accounts_customuser` table. This likely happened because the database schema is not in sync with your Django models.

## Quick Fix for Conflicting Migrations

If you're seeing the error "Conflicting migrations detected", run:

```bash
python fix_conflicting_migrations.py
```

This script will:
1. Create a merge migration to resolve the conflicts
2. Apply all migrations

## Comprehensive Fix

For a more thorough fix that addresses potential database schema issues:

```bash
python comprehensive_fix.py
```

This script will:
1. Backup all migration files
2. Check the database state
3. Fix the database directly if needed
4. Reset migrations in the database
5. Clean up migration files
6. Create a new migration to fix the hospital field
7. Apply all migrations

## Verify the Fix

After applying either fix, verify that everything is working correctly:

```bash
python verify_fix.py
```

This script will:
1. Check if required columns exist in the database
2. Check migrations in the database
3. Check user-hospital relationships

## Manual Fix Options

### Option 1: Merge conflicting migrations

```bash
python manage.py makemigrations --merge
python manage.py migrate
```

### Option 2: Reset and recreate migrations

```bash
# Backup your migrations first!
python manage.py migrate accounts zero
python manage.py makemigrations accounts
python manage.py migrate accounts
```

### Option 3: Fix the database directly

Connect to your MySQL database:
```bash
mysql -u root -p
```

Use the medical_tracking database:
```sql
USE medical_tracking;
```

Add the hospital_id column if it doesn't exist:
```sql
ALTER TABLE accounts_customuser 
ADD COLUMN hospital_id INT NULL,
ADD CONSTRAINT fk_hospital 
FOREIGN KEY (hospital_id) 
REFERENCES accounts_hospital(hospital_id) 
ON DELETE SET NULL;
```

Add the is_doctor column if it doesn't exist:
```sql
ALTER TABLE accounts_customuser 
ADD COLUMN is_doctor BOOLEAN DEFAULT FALSE;
```

## Troubleshooting

If you still encounter issues:

1. Check the database schema:
   ```sql
   DESCRIBE accounts_customuser;
   ```

2. Check the migration history:
   ```sql
   SELECT * FROM django_migrations WHERE app='accounts';
   ```

3. Check for foreign key constraints:
   ```sql
   SELECT * FROM information_schema.key_column_usage
   WHERE referenced_table_name = 'accounts_hospital';
   ```

4. Verify the existence of the `hospital_id` column before attempting to drop it:
   ```sql
   SELECT COLUMN_NAME 
   FROM INFORMATION_SCHEMA.COLUMNS 
   WHERE TABLE_NAME = 'accounts_customuser' AND COLUMN_NAME = 'hospital_id';
   ```

   If the column does not exist, remove or modify the migration step that attempts to drop it.

5. If all else fails, you might need to recreate the database:
   ```sql
   DROP DATABASE medical_tracking;
   CREATE DATABASE medical_tracking;
   ```
   Then run:
   ```bash
   python manage.py migrate
   ```