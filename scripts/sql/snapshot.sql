DELETE FROM raw.raw_customer_addresses WHERE id = 3;
INSERT INTO raw.raw_customer_addresses (id, user_id, city, updated_at,_etl_loaded_at) VALUES (3, 1, 'Berlin', '2023-02-01',NOW())