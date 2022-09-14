
import scrapy
# from items import Car
import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname('dealerships_scraper')))
import items

class IrwinAutoGroupSpider(scrapy.Spider):
  name = "irwin_auto_group"
  start_urls = [
      'https://www.irwinzone.com/searchused.aspx?pn=50',
  ]

  DEALERSHIP_INFO = {
    'dealership_name': 'Irwin Automotive Group',
    'address': '59 Bisson Avenue',
    'zipcode': '03246',
    'city': 'Laconia',
    'state': 'NH'
  }

  def parse(self, response):
    selectors = response.xpath("//div[@class='row srpVehicle hasVehicleInfo']")
    for selector in selectors:
      yield from self.parse_car(selector, response.url)

    # https://www.irwinzone.com/searchused.aspx?pn=50&pt=2
    next_page = response.xpath("//a[@class='stat-arrow-next']/@href").extract()[0]

    # # Additional layer of logic required to correctly retrieve the next url:
    print("Next Page: ", next_page)
    if next_page:
      next_page_url = f"https://www.irwinzone.com{next_page}"
      yield scrapy.Request(
          url=next_page_url,
          callback=self.parse
      )
    else:
      print('No more pages to scrape')

  def parse_car(self, response, current_url):
    item = items.Car()

    # Parse title
    title = response.xpath("@data-name").extract()[0].strip()
    item['title'] = title if title else None

    year = response.xpath("@data-year").extract()[0]
    year = int(year)
    item['year'] = year if year else None

    make = response.xpath("@data-make").extract()[0].strip()
    item['make'] = make if make else None

    model = response.xpath("@data-model").extract()[0].strip()
    item['model'] = model if model else None

    trim = response.xpath("@data-trim").extract()[0].strip()
    item['trim'] = trim if trim else None

    price = response.xpath("@data-price").extract()[0].strip()
    item['price'] = float(price) if price else None

    vehicle_type = response.xpath("@data-bodystyle").extract()[0].strip()
    item['vehicle_type'] = vehicle_type if vehicle_type else None

    item['model_trim'] = item['make'] + ' ' + item['model']

    mileage = response.xpath("@data-mileage").extract()[0]
    item['mileage'] = int(mileage) if mileage else None

    interior_color = response.xpath("@data-intcolor").extract()[0].strip()
    item['interior_color'] = interior_color if interior_color else None

    exterior_color = response.xpath("@data-extcolor").extract()[0].strip()
    item['exterior_color'] = exterior_color if exterior_color else None

    drivetrain = response.xpath("@data-drivetrain").extract()[0].strip()
    item['drivetrain'] = drivetrain if drivetrain else None

    transmission = response.xpath("@data-trans").extract()[0].strip()
    item['transmission'] = transmission if transmission else None

    engine = response.xpath("@data-engine").extract()[0].strip()
    item['engine'] = engine if engine else None

    vin = response.xpath("@data-vin").extract()[0].strip()
    item['vin'] = vin if vin else None

    item['dealership_name'] = self.DEALERSHIP_INFO['dealership_name']
    item['dealership_address'] = self.DEALERSHIP_INFO['address']
    item['dealership_zipcode'] = self.DEALERSHIP_INFO['zipcode']
    item['dealership_city'] = self.DEALERSHIP_INFO['city']
    item['dealership_state'] = self.DEALERSHIP_INFO['state']
    item['scraped_url'] = current_url
    item['scraped_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    yield item
