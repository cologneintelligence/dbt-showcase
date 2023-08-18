DELETE FROM raw.raw_analytics WHERE id = 6;
INSERT INTO raw.raw_analytics (id, customer_id, event, timestamp,_etl_loaded_at) VALUES (6, 1, 'VISIT_HOMEPAGE', '2023-01-02 15:00:00',NOW());