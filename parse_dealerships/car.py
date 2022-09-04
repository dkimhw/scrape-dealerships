from scrapy import Item, Field

class Car(Item):
  title = Field()
  year = Field()
  make = Field()
  model = Field()
  trim = Field()
