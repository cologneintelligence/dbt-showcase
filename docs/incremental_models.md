## Incremental Models

Incremental models are dbt's way of handling large models, that take too much time to process their respective data. An incremental model does not recompute the whole table on every run, but only the data that arrived after the model was last run.

The usual way of thinking is: First, materialize a model as a view. If it takes too much time to query, materialize it as a table. If it takes too much time to build, materialize it as an incremental table.

Take for example an analytics table, which receives new analytics data about customer behavior on the shop website every day. An incremental model does not recompute the whole analytics table containing x years worth of data, but only the rows which arrived since the last model run. This reduces the time a model takes to process new data and saves costs with your respective cloud provider.

For more in-depth information on incremental models and how to use them, see the following links:

- [Incremental models | dbt Developer Hub](https://docs.getdbt.com/docs/build/incremental-models)
- [dbt Incremental Strategies | Indicium Engineering](https://medium.com/indiciumtech/understanding-dbt-incremental-strategies-part-2-2-add59889ea17)

For a practical example with fictional analytics data, perform the following steps:

```bash
# 1. Run the database control script to reset your database
python demo.py -o reset 

cd jaffle_shop

# 2. Trigger the usual dbt workflow
dbt snapshot
dbt run --full-refresh

cd ..

# 3. Run incremental_simulator.ipynb to simulate newly arrived data from a web analytics framework
python demo.py -o inc

cd jaffle_shop

# 4. Trigger the incremental model
dbt run --select stg_analytics
```

**Involved tables**

`raw.raw_analytics`: The raw data table which holds data from the fictional analytics framework. In a real scenario, this table would be very large with several million rows, describing user behavior on the shop website. Most important here is the `timestamp` column, which enables us to comprehend, when a row was created. Based on this, the incremental model decides which rows have to be processed.

`dbt_postgres_staging.stg_analytics`: The table built as a result of the incremental model. It contains analytics data which, for learning purposes, was enriched by customer data. When working with large tables and complex joins or transformations, it makes sense to use incremental models if possible.

**Explanation**

1. Reset your database and make sure that you're working on a clean workspace
2. Create the status quo by running dbt in full-refresh mode. This recomputes all models and incremental models are not run incrementally but process all data they have available.
3. Simulate the arrival of new data in `raw.raw_analytics` table. The timestamp of the now row is larger than the maximum of the timestamp column in `dbt_postgres_staging.stg_analytics`.
4. Re-running the incremental model (Not in full refresh mode!) leads to it processing the newest data in `raw.raw_analytics`. It identifies the newest data by filtering for all rows which timestamp is newer than the newest row in `dbt_postgres_staging.stg_analytics` according to the timestamp column.