CREATE DATABASE IF NOT EXISTS vivid_seats;
use vivid_seats;

CREATE TABLE IF NOT EXISTS seller(
    seller_id INT AUTO_INCREMENT,
    seller_name VARCHAR(255) NOT NULL UNIQUE,
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(seller_id)
);

CREATE TABLE IF NOT EXISTS event(
    event_id INT AUTO_INCREMENT,
    event_name VARCHAR(500) NOT NULL UNIQUE,
    event_street VARCHAR(500) NOT NULL,
    event_city VARCHAR(100) NOT NULL,
    event_state VARCHAR(100) NOT NULL,
    event_country VARCHAR(100) NOT NULL,
    event_zip VARCHAR(5) NOT NULL,
    event_time DATETIME NOT NULL,
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(event_id)
);

CREATE TABLE IF NOT EXISTS ticket(
    ticket_id INT AUTO_INCREMENT,
    event_id INT NOT NULL,
    seller_id INT NOT NULL,
    ticket_section SMALLINT NOT NULL,
    ticket_row VARCHAR(10) NOT NULL,
    ticket_quantity INT NOT NULL,
    ticket_price DECIMAL(10, 2) NOT NULL,
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(ticket_id),
    FOREIGN KEY fk_event_ticket(event_id) REFERENCES event(event_id),
    FOREIGN KEY fk_seller_ticket(seller_id) REFERENCES seller(seller_id),
    UNIQUE KEY (event_id, seller_id, ticket_section, ticket_row, ticket_price)
);

CREATE TABLE IF NOT EXISTS referal(
    referal_id INT AUTO_INCREMENT,
    referal_name VARCHAR(255) NOT NULL UNIQUE,
    PRIMARY KEY(referal_id)
);

CREATE TABLE IF NOT EXISTS customer(
    customer_id INT AUTO_INCREMENT,
    customer_name VARCHAR(255) NOT NULL UNIQUE,
    customer_street VARCHAR(500),
    customer_city VARCHAR(100),
    customer_state VARCHAR(100),
    customer_country VARCHAR(100),
    customer_zip VARCHAR(5),
    customer_phone VARCHAR(20),
    customer_email VARCHAR(255),
    referal_id INT,
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(customer_id)
);

CREATE TABLE IF NOT EXISTS order_status(
    status_id TINYINT AUTO_INCREMENT,
    status_name VARCHAR(255) NOT NULL UNIQUE,
    PRIMARY KEY(status_id)
);

CREATE TABLE IF NOT EXISTS `order`(
    order_id INT AUTO_INCREMENT,
    customer_id INT NOT NULL,
    referal_id INT NOT NULL,
    ticket_id INT NOT NULL,
    order_quantity INT NOT NULL,
    order_total_price DECIMAL(10, 2) NOT NULL,
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    order_status TINYINT,
    PRIMARY KEY(order_id),
    FOREIGN KEY fk_customer_order(customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY fk_referal_order(referal_id) REFERENCES referal(referal_id),
    FOREIGN KEY fk_status_order(order_status) REFERENCES order_status(status_id),
    FOREIGN KEY fk_ticket_order(ticket_id) REFERENCES ticket(ticket_id)
);
