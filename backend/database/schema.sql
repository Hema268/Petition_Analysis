CREATE DATABASE IF NOT EXISTS petition_system;

USE petition_system;

CREATE TABLE IF NOT EXISTS petitions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    extracted_text TEXT NOT NULL,
    department VARCHAR(100),
    priority ENUM('low', 'medium', 'high') DEFAULT 'low',
    cluster VARCHAR(50),
    sentiment VARCHAR(50),
    status ENUM('pending', 'in_progress', 'resolved') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
