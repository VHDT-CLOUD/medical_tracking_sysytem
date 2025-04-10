SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS django_migrations;
DROP TABLE IF EXISTS accounts_customuser;
DROP TABLE IF EXISTS accounts_doctor;
DROP TABLE IF EXISTS accounts_patient;
DROP TABLE IF EXISTS accounts_medicalrecord;
DROP TABLE IF EXISTS accounts_medicaldocument;
DROP TABLE IF EXISTS accounts_profile;
DROP TABLE IF EXISTS accounts_hospital;
DROP TABLE IF EXISTS django_admin_log;
DROP TABLE IF EXISTS django_content_type;
DROP TABLE IF EXISTS django_session;
DROP TABLE IF EXISTS auth_group;
DROP TABLE IF EXISTS auth_group_permissions;
DROP TABLE IF EXISTS auth_permission;

SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE django_migrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied DATETIME NOT NULL
); 