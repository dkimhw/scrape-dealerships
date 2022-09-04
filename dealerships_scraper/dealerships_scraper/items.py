# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Car(scrapy.Item):
  title = scrapy.Field()
  year = scrapy.Field()
  make = scrapy.Field()
  model = scrapy.Field()
  trim = scrapy.Field()
  price = scrapy.Field()
  vehicle_type = scrapy.Field()
  model_trim = scrapy.Field()
  vehicle_mileage = scrapy.Field()
  exterior_color = scrapy.Field()
  interior_color = scrapy.Field()
  transmission = scrapy.Field()
  engine = scrapy.Field()
  drivetrain = scrapy.Field()
  vin = scrapy.Field()
