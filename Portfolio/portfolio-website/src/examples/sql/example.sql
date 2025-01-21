-- SQL example for creating a simple database and table

CREATE DATABASE portfolio;

USE portfolio;

CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO projects (title, description) VALUES
('HTML Portfolio', 'A portfolio showcasing my HTML skills.'),
('Python Script', 'A Python script for data analysis.'),
('SQL Database', 'An example of SQL database creation and management.');