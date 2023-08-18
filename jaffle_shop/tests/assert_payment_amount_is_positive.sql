-- Payments should always be >= 0 in order for transactions to be correct
-- This test PASSES if NO rows are returned

SELECT *
FROM {{ ref('stg_payments') }} 
WHERE amount < 0