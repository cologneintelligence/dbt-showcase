with source as (
    
    select * from {{ source('cashing_system', 'raw_payments') }}

),

renamed as (

    select
        id as payment_id,
        order_id as order_id,
        payment_method as payment_method,
        -- simplify payment_type from payment_method
        case
            when payment_method in ('stripe', 'paypal', 'credit_card', 'gift_card') then 'credit'
            else 'cash'
        end as payment_type,
        status,
        
        -- `amount` is currently stored in cents, so we convert it to dollars
        amount as amount_cents,
        amount / 100 as amount,

        case
            when status = 'successful' then true
            else false
        end as is_completed_payment,

        date_trunc('day', created) as created_date,

        created as created_at
        

    from source

)

select * from renamed