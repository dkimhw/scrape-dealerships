import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import sqlite3
import numpy as np

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


conn = sqlite3.connect('../database/cars_test.db')

sql_query = '''

select dealership_name, count(*) from inventory group by 1;

'''
result = pd.read_sql_query(sql_query, conn)
print(result)


import datetime
end_date =  datetime.date.today()
y = datetime.date(end_date.year, end_date.month, 1).strftime("%Y-%m-%d")
# curr_beg_month = datetime.today().replace(day=1)
# print(curr_beg_month)
print("y", y)

query2 = f"select vin, DATE(scraped_date, 'start of month') from inventory where vin = '19UDE2F34LA004973' and DATE(scraped_date, 'start of month') = '{y}'"
#query2 = "select vin from inventory limit 1"
result2 = pd.read_sql_query(query2, conn)
print(result2)
# drop_query = '''
# drop table inventory
# '''

# cur = conn.cursor()
# cur.execute(drop_query)
# conn.commit()

####### Drop Table

# TABLE_NAME = 'inventory_test'
# DB_NAME = './dealerships_scraper/data/cars_test.db'

# #Connecting to sqlite
# conn = sqlite3.connect(DB_NAME)

# #Creating a cursor object using the cursor() method
# cursor = conn.cursor()

# #Doping EMPLOYEE table if already exists
# cursor.execute(f"DROP TABLE {TABLE_NAME}")
# print("Table dropped... ")

# #Commit your changes in the database
# conn.commit()

# #Closing the connection
# conn.close()
