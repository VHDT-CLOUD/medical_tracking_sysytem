# Hospital Setup Guide (Updated)

This guide will help you add hospital details to the database and set up hospital login credentials.

## Adding a Hospital

To add a hospital to the database, use the `add_hospital_new` management command:

```bash
python manage.py add_hospital_new --name "Hospital Name" --email "hospital@example.com" --address "Hospital Address" --registration_number "REG12345" --password "secure_password"
```

Example:
```bash
python manage.py add_hospital_new --name "City General Hospital" --email "info@citygeneral.com" --address "123 Main Street, City" --registration_number "CGH2023001" --password "hospital123"
```

This will:
1. Create a new hospital record in the database
2. Create a CustomUser account for the hospital
3. Set the password for the hospital login

## Hospital Login

Once you've added a hospital, you can log in using:

1. Registration Number: The registration number you provided when adding the hospital
2. Password: The password you provided when adding the hospital

## Example Setup

Here's a complete example of setting up a hospital:

```bash
# Add the hospital with all required information including password
python manage.py add_hospital_new --name "City General Hospital" --email "info@citygeneral.com" --address "123 Main Street, City" --registration_number "CGH2023001" --password "hospital123"
```

After running this command, you can log in to the hospital dashboard using:
- Registration Number: CGH2023001
- Password: hospital123

## Making Database Migrations

If you've made changes to the models, make sure to run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

This will update your database schema to include the new fields and relationships.