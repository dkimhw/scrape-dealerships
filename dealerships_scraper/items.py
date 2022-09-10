# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Car(scrapy.Item):
  vin = scrapy.Field()
  title = scrapy.Field()
  year = scrapy.Field()
  make = scrapy.Field()
  model = scrapy.Field()
  trim = scrapy.Field()
  model_trim = scrapy.Field()
  price = scrapy.Field()
  mileage = scrapy.Field()
  vehicle_type = scrapy.Field()
  exterior_color = scrapy.Field()
  interior_color = scrapy.Field()
  transmission = scrapy.Field()
  engine = scrapy.Field()
  drivetrain = scrapy.Field()
  dealership_name = scrapy.Field()
  dealership_address = scrapy.Field()
  dealership_zipcode = scrapy.Field()
  dealership_city = scrapy.Field()
  dealership_state = scrapy.Field()
  scraped_url = scrapy.Field()
  scraped_date = scrapy.Field()
