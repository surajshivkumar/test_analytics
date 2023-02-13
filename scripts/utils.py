import psycopg2
import configparser
import pandas as pd
def get_confg(path: str):
    config = configparser.ConfigParser()
    _ = config.read(path)
    return config

def get_sql_conn(sql_conf: configparser.SectionProxy, dbname: str = None):
    if dbname is None:
        dbname = sql_conf.get('dbname')
    prodution_db = psycopg2. \
        connect(host=sql_conf['host'],
                database=dbname,
                user=sql_conf['user'],
                password=sql_conf['password'])
    return prodution_db


def push_to_sql(data: pd.DataFrame, config: configparser.ConfigParser,section):
    table = config[section]['table']
    pk = config[section]['pk']
    df_columns = list(data)
    columns = ",".join(df_columns)
    values = "VALUES({})".format(",".join(["%s" for _ in df_columns]))
    updates = ','.join([col + '=excluded.' + col for col in df_columns])
    insert_stmt = "INSERT INTO {} ({}) {} ON CONFLICT ({}) DO UPDATE SET {}". \
        format(table, columns, values, pk, updates)
    conn = get_sql_conn(config['sql-prod'],
                        config.get('sql-prod', 'dbname'))
    cur = conn.cursor()
    psycopg2.extras.execute_batch(cur, insert_stmt, data.values)
    conn.commit()
    cur.close()
    conn.close()