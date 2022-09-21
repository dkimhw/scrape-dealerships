# Define your item pipelines here
import psycopg2
from config import settings
import datetime

class DealershipsScraperPipeline:
  def __init__(self):
    ## Create/Connect to database
    self.con = psycopg2.connect(user = settings.username, password = settings.password , host= settings.host, port = settings.port, database = settings.database)

    ## Create cursor, used to execute commands
    self.cur = self.con.cursor()

    ## Create quotes table if none exists
    self.cur.execute("""
    CREATE TABLE IF NOT EXISTS scraped_datasets.scraped_inventory_data.inventories (
        vin varchar NOT NULL,
        title varchar,
        year integer,
        make varchar,
        model varchar,
        trim varchar,
        model_trim varchar,
        price money,
        mileage integer,
        vehicle_type varchar,
        interior_color varchar,
        exterior_color varchar,
        transmission varchar,
        engine varchar,
        drivetrain varchar,
        dealership_name varchar,
        dealership_address varchar,
        dealership_zipcode varchar,
        dealership_city varchar,
        dealership_state varchar,
        scraped_url varchar,
        scraped_date timestamp,
        scraped_month date not null,
        CONSTRAINT inventories_pk PRIMARY KEY (vin, scraped_month)
    )
    """)

  def process_item(self, item, spider):
    curr_date =  datetime.date.today()
    beg_month = datetime.date(curr_date.year, curr_date.month, 1).strftime("%Y-%m-%d")

    ## Check to see if text is already in database
    self.cur.execute("select * from scraped_inventory_data.inventories where vin = %s and date_trunc('month', scraped_date) = %s", (item['vin'], beg_month))
    result = self.cur.fetchone()

    ## If it is in DB, create log message
    if result:
      spider.logger.warn("Item already in database: %s" % item['vin'])
    else:
      self.cur.execute("""
          INSERT INTO scraped_inventory_data.inventories
            (vin, title, year, make, model
            , trim, model_trim, price, mileage
            , vehicle_type, interior_color, exterior_color
            , transmission, engine, drivetrain, dealership_name
            , dealership_address, dealership_zipcode, dealership_city
            , dealership_state, scraped_url, scraped_date, scraped_month)
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
      """,
      (
          item['vin'], item['title'], item['year'], item['make'], item['model']
          , item['trim'], item['model_trim'], item['price'], item['mileage']
          , item['vehicle_type'], item['interior_color'], item['exterior_color']
          , item['transmission'], item['engine'], item['drivetrain']
          , item['dealership_name'], item['dealership_address'], item['dealership_zipcode']
          , item['dealership_city'], item['dealership_state'], item['scraped_url']
          , item['scraped_date'], beg_month
      ))

      ## Execute insert of data into database
      self.con.commit()
    return item
