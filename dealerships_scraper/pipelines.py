# Define your item pipelines here
import sqlite3
import datetime

class DealershipsScraperPipeline:
  def __init__(self):
    ## Create/Connect to database
    self.con = sqlite3.connect('../database/cars.db')

    ## Create cursor, used to execute commands
    self.cur = self.con.cursor()

    ## Create quotes table if none exists
    self.cur.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        vin TEXT NOT NULL,
        title TEXT,
        year INTEGER,
        make TEXT,
        model TEXT,
        trim TEXT,
        model_trim TEXT,
        price REAL,
        mileage INTEGER,
        vehicle_type TEXT,
        interior_color TEXT,
        exterior_color TEXT,
        transmission TEXT,
        engine TEXT,
        drivetrain TEXT,
        dealership_name TEXT,
        dealership_address TEXT,
        dealership_zipcode TEXT,
        dealership_city TEXT,
        dealership_state TEXT,
        scraped_url TEXT,
        scraped_date TEXT
    )
    """)

  def process_item(self, item, spider):
    curr_date =  datetime.date.today()
    beg_month = datetime.date(curr_date.year, curr_date.month, 1).strftime("%Y-%m-%d")

    ## Check to see if text is already in database
    self.cur.execute("select * from inventory where vin = ? and DATE(scraped_date, 'start of month') = ?", (item['vin'], beg_month, ))
    result = self.cur.fetchone()

    ## If it is in DB, create log message
    if result:
      spider.logger.warn("Item already in database: %s" % item['vin'])
    else:
      self.cur.execute("""
          INSERT INTO inventory
            (vin, title, year, make, model
            , trim, model_trim, price, mileage
            , vehicle_type, interior_color, exterior_color
            , transmission, engine, drivetrain, dealership_name
            , dealership_address, dealership_zipcode, dealership_city
            , dealership_state, scraped_url, scraped_date)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      """,
      (
          item['vin'], item['title'], item['year'], item['make'], item['model']
          , item['trim'], item['model_trim'], item['price'], item['mileage']
          , item['vehicle_type'], item['interior_color'], item['exterior_color']
          , item['transmission'], item['engine'], item['drivetrain']
          , item['dealership_name'], item['dealership_address'], item['dealership_zipcode']
          , item['dealership_city'], item['dealership_state'], item['scraped_url']
          , item['scraped_date']
      ))

      ## Execute insert of data into database
      self.con.commit()
    return item
