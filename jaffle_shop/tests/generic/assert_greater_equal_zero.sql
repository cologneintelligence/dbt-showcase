-- A column should have values that are either posive or zero

{% test greater_equal_zero(model, column_name) %}

SELECT *
FROM {{ model }} 
WHERE {{ column_name }} < 0

{% endtest %}