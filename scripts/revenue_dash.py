import pandas as pd
import numpy as np
import os
import psycopg2
import psycopg2.extras
import configparser
import sys
import time
from utils import get_confg, push_to_sql,get_sql_conn 
import warnings
warnings.filterwarnings("ignore")


def get_data(config):
    # create connection to prod table
    prod_conn = get_sql_conn(config['sql-prod'])
    #read required tables
    order_items = pd.read_sql('''select * from order_items''',prod_conn)
    order_details = pd.read_sql('''select * from orders''',prod_conn)

    #flow
    all_orders = pd.merge(order_items, order_details,on='order_id',how='inner')
    all_orders['total_price'] = all_orders.quantity * all_orders.unit_price

    result = all_orders.groupby(['order_date']).agg(revenue = ('total_price','sum'),
                                                    total_items = ('quantity','sum'))
    result = result.reset_index()
    result['AOV'] = result.revenue / result.total_items

    table_alias = 'yulu_revenue_'
    result.columns = [table_alias + col for col in result.columns] 
    return result

def main(conf_path:str):
    start_time = time.time()
    config = get_confg(conf_path)
    data = get_data(config)
    push_to_sql(data, config,'materialized-view','overall_rev')
    time_taken   = time.time() - start_time
    print('Time taken = {} s'.format(round(time_taken,1)))

if __name__ == '__main__':
    main(*sys.argv[1:])