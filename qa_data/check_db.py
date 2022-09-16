import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import sqlite3
import numpy as np

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


conn = sqlite3.connect('../database/cars.db')
end_date =  datetime.date.today()
y = datetime.date(end_date.year, end_date.month, 1).strftime("%Y-%m-%d")
sql_query = f'''

select
  dealership_name, count(*) from inventory
  where
 DATE(scraped_date, 'start of month') = '{y}'
 group by 1;

'''
result = pd.read_sql_query(sql_query, conn)
print("Number of cars scraped per dealership for the month of " + y)
print(result)


print()
print("All cars in database")
all_cars = f'''

select
  dealership_name, count(*) from inventory
 group by 1;

'''
inv = pd.read_sql_query(all_cars, conn)
print(inv)


print()
print("All cars in database per month")
avg_scrape_per_month = f'''

select
  dealership_name, count(*)/count(distinct DATE(scraped_date, 'start of month')) as avg_scraped_inv from inventory
 group by 1;

'''
avg_scrape = pd.read_sql_query(avg_scrape_per_month, conn)
print(avg_scrape)


# import datetime

# # curr_beg_month = datetime.today().replace(day=1)
# # print(curr_beg_month)

# query2 = f"select rowid, vin, DATE(scraped_date, 'start of month') from inventory where vin = '19UDE2F34LA004973' and DATE(scraped_date, 'start of month') = '{y}'"
# result2 = pd.read_sql_query(query2, conn)
# print(result2)


# query2 = f"select rowid, vin, scraped_date, year, make, model, trim, mileage, price from inventory where dealership_name = 'Avon Auto Brokers' and DATE(scraped_date, 'start of month') = '{y}'"
# result2 = pd.read_sql_query(query2, conn)
# print()
# print(result2)



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
