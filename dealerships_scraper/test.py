
import sys

sys.path.insert(0, '../')

import psycopg2
from config import settings
import datetime

curr_date =  datetime.date.today()
beg_month = datetime.date(curr_date.year, curr_date.month, 1).strftime("%Y-%m-%d")
print(beg_month)
con = psycopg2.connect(user = settings.username, password = settings.password , host= settings.host, port = settings.port, database = settings.database)
cur = con.cursor()
cur.execute(f"select distinct dealership_name from scraped_inventory_data.inventories where date_trunc('month', scraped_date) = '{beg_month}'")
result = list(cur.fetchall())
print("result: ", result)
# Call
cur.execute("select distinct dealership_name from scraped_inventory_data.inventories")
compare = list(cur.fetchall())

print("compare: ", compare)
