-- Drop the existing table
DROP TABLE IF EXISTS accounts_hospital;

-- Create the table with all required fields
CREATE TABLE accounts_hospital (
    hospital_id INT AUTO_INCREMENT PRIMARY KEY,
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