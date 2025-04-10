-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS medical_tracking;

-- Create a new user with proper permissions
CREATE USER IF NOT EXISTS 'medical_user'@'localhost' IDENTIFIED BY 'medical@123';

-- Grant all privileges on the medical_tracking database to the new user
GRANT ALL PRIVILEGES ON medical_tracking.* TO 'medical_user'@'localhost';

-- Apply the changes
FLUSH PRIVILEGES;

-- Switch to the medical_tracking database
USE medical_tracking; 