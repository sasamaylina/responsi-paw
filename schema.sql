-- Schema SQL untuk Sistem Donasi
-- Database: SQLite

-- Tabel User
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    role VARCHAR(20) DEFAULT 'donor',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabel Campaign
CREATE TABLE campaign (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    target_amount FLOAT NOT NULL,
    collected_amount FLOAT DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabel Donation (berelasi dengan User dan Campaign)
CREATE TABLE donation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    campaign_id INTEGER NOT NULL,
    amount FLOAT NOT NULL,
    message TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (campaign_id) REFERENCES campaign(id) ON DELETE CASCADE
);

-- Index untuk optimasi query
CREATE INDEX idx_donation_user ON donation(user_id);
CREATE INDEX idx_donation_campaign ON donation(campaign_id);
CREATE INDEX idx_user_role ON user(role);
CREATE INDEX idx_campaign_active ON campaign(is_active);

-- Contoh data awal
INSERT INTO user (username, email, password_hash, role) 
VALUES ('admin', 'admin@example.com', 'hashed_password_here', 'admin');

INSERT INTO campaign (title, description, target_amount, collected_amount, is_active)
VALUES ('Bantuan Bencana Alam', 'Donasi untuk korban bencana alam', 10000000, 0, 1);
