-- SQL schema for storing income data by major --
CREATE TABLE income_by_major (
    id INT AUTO_INCREMENT PRIMARY KEY,
    major VARCHAR(255) NOT NULL UNIQUE,
    income INT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_income (income),
    INDEX idx_timestamp (timestamp)
);