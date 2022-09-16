
import pandas as pd
import datetime
import sqlite3
import numpy as np


conn = sqlite3.connect('../database/cars.db')
end_date =  datetime.date.today()
start_of_month = datetime.date(end_date.year, end_date.month, 1).strftime("%Y-%m-%d")


query = '''
    select
      dealership_name, count(*) as count
    from
      (
        SELECT
          *
          , row_number() OVER (PARTITION BY vin, DATE(scraped_date, 'start of month')  ORDER BY scraped_date desc) AS filter_row
        FROM inventory_load
        WHERE
          vin is not null
          and scraped_date < '2022-09-01'
      )
    where filter_row = 1
    group by 1
'''
tbl = pd.read_sql_query(query, conn)
print(tbl)


# upload_query = """
#     INSERT INTO inventory (
#       vin, title, year, make, model, trim, model_trim
#       , price, mileage, vehicle_type, interior_color, exterior_color
#       , transmission, engine, drivetrain, dealership_name
#       , dealership_address, dealership_zipcode, dealership_city
#       , dealership_state, scraped_url, scraped_date
#     )

#     select
#       vin, title, year, make, model, trim, model_trim
#       , price, vehicle_mileage, vehicle_type, interior_color, exterior_color
#       , transmission, engine, drivetrain, dealership_name
#       , dealership_address, dealership_zipcode, dealership_city
#       , dealership_state, inventory_load_url, scraped_date
#     from
#       (
#         SELECT
#           *
#           , row_number() OVER (PARTITION BY vin, DATE(scraped_date, 'start of month')  ORDER BY scraped_date desc) AS filter_row
#         FROM inventory_load
#         WHERE
#           vin is not null
#           and scraped_date < '2022-09-01'
#       )
#     where filter_row = 1
# """
# cur = conn.cursor()
# cur.execute(upload_query)
# conn.commit()
