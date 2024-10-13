-- Tạo người dùng mới
CREATE USER 'dbuser'@'localhost' IDENTIFIED BY '123';

-- Cấp quyền cho người dùng trên cơ sở dữ liệu testdb
GRANT ALL PRIVILEGES ON testdb.* TO 'dbuser'@'localhost';

-- Làm mới quyền
FLUSH PRIVILEGES;

CREATE DATABASE IF NOT EXISTS testdb;
USE testdb;

CREATE TABLE IF NOT EXISTS sample_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data VARCHAR(255) NOT NULL
);

INSERT INTO sample_table (data) VALUES 
('Data 1'),
('Data 2'),
('Data 3'),
('Data 4'),
('Data 5');