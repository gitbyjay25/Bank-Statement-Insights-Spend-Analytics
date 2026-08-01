USE bank_insights;

CREATE TABLE IF NOT EXISTS statements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    account_label VARCHAR(100),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    statement_id INT NOT NULL,
    txn_date DATE NOT NULL,
    description VARCHAR(500) NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    txn_type ENUM('debit', 'credit') NOT NULL,
    category VARCHAR(100),
    confidence_score DECIMAL(4, 3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (statement_id) REFERENCES statements(id)
);

CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    bucket ENUM('mandatory', 'non_mandatory', 'investment', 'income') NOT NULL
);

CREATE TABLE IF NOT EXISTS category_rules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    keyword VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    learned_from_user BOOLEAN DEFAULT FALSE
);

INSERT INTO categories (name, bucket) VALUES
('Food & Dining', 'non_mandatory'),
('Transport', 'non_mandatory'),
('Shopping', 'non_mandatory'),
('Entertainment', 'non_mandatory'),
('Rent & Housing', 'mandatory'),
('Utilities', 'mandatory'),
('EMI & Loans', 'mandatory'),
('Healthcare', 'mandatory'),
('Investment', 'investment'),
('Income', 'income'),
('Other', 'non_mandatory');

INSERT INTO category_rules (keyword, category) VALUES
('SWIGGY', 'Food & Dining'),
('ZOMATO', 'Food & Dining'),
('UBER', 'Transport'),
('OLA', 'Transport'),
('AMAZON', 'Shopping'),
('FLIPKART', 'Shopping'),
('NETFLIX', 'Entertainment'),
('SPOTIFY', 'Entertainment'),
('ELECTRICITY', 'Utilities'),
('WATER', 'Utilities'),
('RENT', 'Rent & Housing'),
('EMI', 'EMI & Loans'),
('SIP', 'Investment'),
('SALARY', 'Income');