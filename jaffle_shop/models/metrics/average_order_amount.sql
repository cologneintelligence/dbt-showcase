select * 
from {{ metrics.calculate(
    metric('average_order_amount'),
    grain='month',
    dimensions=['status'],
) }}