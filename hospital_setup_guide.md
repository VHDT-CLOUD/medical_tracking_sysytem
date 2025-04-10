# Hospital Setup Guide

This guide will help you add hospital details to the database and set up hospital login credentials.

## Adding a Hospital

To add a hospital to the database, use the `add_hospital` management command:

```bash
python manage.py add_hospital --name "Hospital Name" --email "hospital@example.com" --contact_number "1234567890" --address "Hospital Address" --registration_number "REG12345"
```

Example:
```bash
python manage.py add_hospital --name "City General Hospital" --email "info@citygeneral.com" --contact_number "9876543210" --address "123 Main Street, City" --registration_number "CGH2023001"
```

This will create a new hospital record in the database and output the hospital ID.

## Setting a Hospital Password

After adding a hospital, you need to set a password for it using the `set_hospital_password_fixed` command:

```bash
python manage.py set_hospital_password_fixed --hospital_id 1 --password "secure_password"
```

Replace `1` with the actual hospital ID that was generated when you added the hospital.

## Hospital Login

Once you've added a hospital and set its password, you can log in using:

1. Hospital ID: The numeric ID generated when adding the hospital
2. Registration Number: The registration number you provided when adding the hospital
3. Password: The password you set using the set_hospital_password_fixed command

## Example Setup

Here's a complete example of setting up a hospital:

```bash
# Add the hospital
python manage.py add_hospital --name "City General Hospital" --email "info@citygeneral.com" --contact_number "9876543210" --address "123 Main Street, City" --registration_number "CGH2023001"

# The command will output something like: "Successfully added hospital: City General Hospital with ID: 1"

# Set the password for the hospital
python manage.py set_hospital_password_fixed --hospital_id 1 --password "hospital123"
```

After running these commands, you can log in to the hospital dashboard using:
- Hospital ID: 1
- Registration Number: CGH2023001
- Password: hospital123