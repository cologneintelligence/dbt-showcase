## Snapshots

Snapshots are the built-in dbt way of handling Slowly-Changing-Dimensions (SCD) type 2. It saves the developer a lot of effort for writing the same code over and over in order to update `valid-from` and `valid-to` database columns. For a more detailed look into dbt Snapshots see the [dbt docs on Snapshots](https://docs.getdbt.com/docs/build/snapshots).

For a practical example, involving the current addresses of some of the Jaffle shop customers, perform the following steps:

```bash
# 1. Run the database control script to reset your database
python demo.py -o reset 

cd jaffle_shop

# 2. Create the initial snapshot table
dbt snapshot

cd ..

# 3. Run the database control script to add a "newly arrived row" to the customer addresses
python demo.py -o snap

cd jaffle_shop

# 4. Create the updated snapshot table
dbt snapshot

# 5. Reload the models
dbt run --full-refresh
```

**Involved tables**

`raw.raw_customer_addresses`: The raw data table which holds the address data. Notice that each entry only holds the customers id, city and when the entry was updated. The "connection" between them, i.e. `valid-from` and `valid-to` gets created later by dbt.

`snapshots.customer_addresses_snapshot`: This table extends the raw table by an SCD-2 type `valid-from` and `valid-to`. It is handled automatically by dbt and updated with the `dbt snapshot` bash command.

`dbt_postgres_staging.stg_customer_addresses`: A sample table which makes use of the SCD-2 information in the snapshot table. It contains the most recent address for every customer in the raw address data.

**Explanation**

1. Reset your database and make sure that you're working on a clean workspace
2. Create the inital snapshot table `snapshots.customer_addresses_snapshot`. The table itself is created and the initial rows from `raw.raw_customer_addresses` are loaded 
3. Simulate the arrival of updated data, i.e. a customer that moved to Berlin. The corresponding row is added in the raw data table `raw.raw_customer_addresses`
4. Update the initial snapshot table. dbt automatically performs a Slowly-Changing-Dimension 2 update for the address of the customer with id 1. The old "Bonn" entry gets invalidated, i.e. the valid-to date is set to the date when the customer moved to Berlin. And the new "Berlin" entry gets inserted into the snapshot table.
5. Compute the models. In `dbt_postgres_staging.stg_customer_addresses` you find the most recent address for each customer in the raw address data.