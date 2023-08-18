{{
    config(
        materialized='incremental'
    )
}}

select
    a.id as analytics_id,
    a.customer_id,
    a.event as website_event,
    a.timestamp as timestamp

from {{ source('jaffle_shop', 'raw_analytics') }} a 


{% if is_incremental() %}

    where a.timestamp > (select max(timestamp) from {{ this }})

{% endif %}