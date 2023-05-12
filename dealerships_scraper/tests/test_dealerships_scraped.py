
import sys
sys.path.insert(0, '../../')
sys.path.insert(0, '../')

import psycopg2
from config import settings
import datetime

class TestScrapedDealerships:
  def test_should_return_true(self):
    # Arrange
    curr_date =  datetime.date.today()
    beg_month = datetime.date(curr_date.year, curr_date.month, 1).strftime("%Y-%m-%d")
    con = psycopg2.connect(user = settings.username, password = settings.password , host= settings.host, port = settings.port, database = settings.database)
    cur = con.cursor()
    cur.execute(f"select distinct dealership_name from scraped_inventory_data.inventories where date_trunc('month', scraped_date) = '{beg_month}'")
    result = list(cur.fetchall())

    # Call
    cur.execute("select distinct dealership_name from scraped_inventory_data.inventories")
    compare = list(cur.fetchall())

    # Print Diff
    list_result = []
    for data in result:
      list_result.append(data[0])

    for dealership in compare:
      if dealership[0] not in list_result:
        print("Missing: ", dealership[0])

    # Assert
    assert len(result) == len(compare)
