Drop Table IF EXISTS raw.raw_customers;
Drop Table IF EXISTS raw.raw_orders;
Drop Table IF EXISTS raw.raw_payments;
Drop Table IF EXISTS raw.raw_customer_addresses;
Drop Table IF EXISTS raw.raw_analytics;



CREATE TABLE IF NOT EXISTS raw.raw_customers(
            id INT PRIMARY KEY,
            first_name VARCHAR,
            last_name VARCHAR,
            _etl_loaded_at TIMESTAMP
        );

CREATE TABLE IF NOT EXISTS raw.raw_orders(
            id INT PRIMARY KEY,
            user_id INT,
            order_date DATE,
            status VARCHAR,
            _etl_loaded_at TIMESTAMP
        );

CREATE TABLE IF NOT EXISTS raw.raw_payments(
            id INT PRIMARY KEY,
            order_id INT,
            payment_method VARCHAR,
            status VARCHAR,
            amount INT,
            created DATE,
            _etl_loaded_at TIMESTAMP
        );

CREATE TABLE IF NOT EXISTS raw.raw_customer_addresses(
            id INT PRIMARY KEY,
            user_id INT,
            city VARCHAR,
            updated_at DATE,
            _etl_loaded_at TIMESTAMP
        );

CREATE TABLE IF NOT EXISTS raw.raw_analytics(
            id INT PRIMARY KEY,
            customer_id INT,
            event VARCHAR,
            timestamp TIMESTAMP,
            _etl_loaded_at TIMESTAMP
        );