CREATE DATABASE IF NOT EXISTS xeroeasy
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_0900_ai_ci;

USE xeroeasy;

CREATE TABLE IF NOT EXISTS students (
    student_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(15) DEFAULT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (student_id),
    UNIQUE KEY uq_students_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS staff (
    staff_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (staff_id),
    UNIQUE KEY uq_staff_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS services (
    service_id INT NOT NULL AUTO_INCREMENT,
    service_name VARCHAR(50) NOT NULL,
    price_per_page DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (service_id),
    UNIQUE KEY uq_services_name (service_name),
    CONSTRAINT chk_services_price CHECK (price_per_page >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS orders (
    order_id INT NOT NULL AUTO_INCREMENT,
    student_id INT NOT NULL,
    service_id INT NOT NULL,
    copies INT NOT NULL,
    status VARCHAR(30) DEFAULT 'Pending',
    order_date TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (order_id),
    KEY ix_orders_student_id (student_id),
    KEY ix_orders_service_id (service_id),
    CONSTRAINT fk_orders_student FOREIGN KEY (student_id)
        REFERENCES students (student_id),
    CONSTRAINT fk_orders_service FOREIGN KEY (service_id)
        REFERENCES services (service_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS deleted_orders (
    order_id INT NOT NULL,
    student_id INT NOT NULL,
    service_id INT NOT NULL,
    copies INT NOT NULL,
    status VARCHAR(30) DEFAULT 'Pending',
    order_date TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (order_id),
    KEY ix_deleted_orders_student_id (student_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO services (service_name, price_per_page) VALUES
    ('Xerox', 2.00),
    ('Printing', 5.00),
    ('Scanning', 3.00),
    ('Color Printing', 10.00),
    ('Photo Copy', 3.00);
