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


conn = sqlite3.connect('../data/cars_test.db')

sql_query = '''

select dealership_name, count(*) from inventory group by 1;

'''
result = pd.read_sql_query(sql_query, conn)
print(result[:3])

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
