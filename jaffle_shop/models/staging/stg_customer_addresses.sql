with source as (
    select * from {{ ref('customer_addresses_snapshot') }}
),

renamed as (
    select
        id as address_id,
        user_id as customer_id,
        city as city,
        updated_at as updated_at,
        dbt_valid_to as dbt_valid_to
    from source 
),

most_recent as (
    select 
        address_id,
        customer_id,
        city,
        updated_at
    from renamed
    where dbt_valid_to is null
)

select * from most_recent