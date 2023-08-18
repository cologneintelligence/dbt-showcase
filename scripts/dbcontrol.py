import psycopg2
import pandas as pd
import datetime as dt
from io import StringIO
import os

host="127.0.0.1"
user="postgres"
pw="postgres"
system_db="postgres"
jaffle_db="jaffle_shop"

sql_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),"sql")



def con_init(host,user,pw,system_db,jaffle_db):
    create_jaffle_db_if_not_exists(host,user,pw,system_db,jaffle_db)

    conn=psycopg2.connect(f"dbname={jaffle_db} user={user} password={pw} host={host}")
    conn.autocommit=True

    return conn

def create_jaffle_db_if_not_exists(host,user,pw,system_db,jaffle_db):
    sys_conn = psycopg2.connect(f"dbname={system_db} user={user} password={pw} host={host}")
    sys_conn.autocommit = True

    #Check if jaffle_db exists
    cur = sys_conn.cursor()
    cur.execute(f"SELECT EXISTS (SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{jaffle_db}')")

    if not cur.fetchone()[0]:
        print(f"{jaffle_db} does not exist - creating...")
        cur.execute(f"CREATE DATABASE {jaffle_db}")
    
    cur.close()
    sys_conn.close()



# Reset schema not database so you can keep the connection open in client (DBeaver)
def reset_schema(conn):
    with conn.cursor() as cur:
        cur.execute("""SELECT schema_name::text
        FROM information_schema.schemata
        where schema_name <> 'public' and schema_name <> 'information_schema' and schema_name !~ '^pg_'""")
        result=cur.fetchall()
        
        for schema in result:
            print(f"Dropping schema {schema[0]}...")
            cur.execute(f"DROP SCHEMA {schema[0]} CASCADE")
        
        print("Creating schema raw...")
        cur.execute("CREATE SCHEMA RAW")

def reset_tables(conn,sql_path):
    with conn.cursor() as cur:
        print("Recreating raw tables...")
        cur.execute(open(os.path.join(sql_path,"tables.sql"),"r").read())

def copy_from_stringio(conn, df, table):
    """
    Here we are going save the dataframe in memory 
    and use copy_from() to copy it to the table
    """
    # save dataframe to an in memory buffer
    buffer = StringIO()
    df.to_csv(buffer, index=False, header=True)
    buffer.seek(0)
    
    with conn.cursor() as cur:
        try:
            cur.copy_expert(f"COPY {table} FROM STDIN WITH CSV HEADER DELIMITER as ','", buffer)
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            conn.rollback()
            return 1
        print(f"Uploading {table} done")
    
def upload_data(conn):
    payments = pd.read_csv("jaffle_shop/seeds/raw_payments.csv")
    payments["_etl_loaded_at"]=dt.datetime.now()
    copy_from_stringio(conn,payments,"raw.raw_payments")
    
    orders = pd.read_csv("jaffle_shop/seeds/raw_orders.csv")
    orders["_etl_loaded_at"]=dt.datetime.now()
    copy_from_stringio(conn,orders,"raw.raw_orders")
    
    customers = pd.read_csv("jaffle_shop/seeds/raw_customers.csv")
    customers["_etl_loaded_at"]=dt.datetime.now()
    copy_from_stringio(conn,customers,"raw.raw_customers")

    customer_addresses = pd.read_csv("jaffle_shop/seeds/raw_customer_addresses.csv")
    customer_addresses["_etl_loaded_at"]=dt.datetime.now()
    copy_from_stringio(conn,customer_addresses,"raw.raw_customer_addresses")

    analytics = pd.read_csv("jaffle_shop/seeds/raw_analytics.csv")
    analytics["_etl_loaded_at"]=dt.datetime.now()
    copy_from_stringio(conn,analytics,"raw.raw_analytics")

def reset():
    conn = con_init(host,user,pw,system_db,jaffle_db)
    try:
        reset_schema(conn)
        reset_tables(conn,sql_path)
        upload_data(conn)
    finally:
        conn.close()

def increment_demo():
    conn = con_init(host,user,pw,system_db,jaffle_db)
    try:
        with conn.cursor() as cur:
            print("Preparing increment demo...")
            cur.execute(open(os.path.join(sql_path,"incremental.sql"),"r").read())
    finally:
        conn.close()
        

def snapshot_demo():
    conn = con_init(host,user,pw,system_db,jaffle_db)
    try:
        with conn.cursor() as cur:
            print("Preparing snapshot demo...")
            cur.execute(open(os.path.join(sql_path,"snapshot.sql"),"r").read())
    finally:
        conn.close()


    