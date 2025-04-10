# Secure Medical Tracking System

A hospital login system for a Secure Medical Tracking System using Node.js/Express, MySQL, HTML, CSS, and JavaScript.

## Features

- Hospital login system
- Patient list view
- Patient dashboard with medical history
- Add medical records functionality
- Session management for security

## Prerequisites

- Node.js (v14 or higher)
- MySQL (v5.7 or higher)
- npm (Node Package Manager)

## Setup Instructions

### 1. Database Setup

Create a MySQL database named `medical_tracking`:

```sql
CREATE DATABASE medical_tracking;
```

The application will automatically create the necessary tables on startup.

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure Database Connection

The application is configured to connect to MySQL with the following default settings:
- Host: localhost
- User: root
- Password: (empty)
- Database: medical_tracking

If your MySQL configuration is different, update the connection details in `server.js`.

### 4. Start the Application

```bash
npm start
```

The server will start on http://localhost:3000

## Usage

### Default Login Credentials

The application creates a default hospital user on first run:
- Email: hospital@example.com
- Password: hospitalpass789

### Accessing the Application

1. Open a web browser and navigate to http://localhost:3000
2. Log in using the default credentials
3. View the list of patients
4. Click on a patient to view their details and medical history
5. Add new medical records as needed

## Project Structure

- `server.js` - Main application file with Express server and MySQL connection
- `public/` - Static files directory
  - `css/style.css` - Main stylesheet
  - `hospital-login.html` - Hospital login page
  - `hospital-patient-list.html` - Patient list page
  - `patient-dashboard.html` - Patient details and medical history page

## Security Notes

For simplicity, this implementation stores passwords in plain text. In a production environment, you should:

1. Use password hashing (e.g., bcrypt)
2. Implement HTTPS
3. Add input validation and sanitization
4. Use environment variables for sensitive information
5. Implement proper error handling and logging