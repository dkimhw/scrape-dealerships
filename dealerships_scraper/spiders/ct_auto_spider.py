
import scrapy
import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname('dealerships_scraper')))
import items
from spiders_utils import get_item_data_from_xpath

class CTAutoSpider(scrapy.Spider):
    name = "ct_auto"
    start_urls = [
      'https://www.ct-auto.com/cars-for-sale-in-Bridgeport-CT-Waterbury-Norwich/used_cars'
    ]

    DEALERSHIP_INFO = {
        'dealership_name': 'CT Auto',
        'address': '7 Wayne Street',
        'zipcode': '06606',
        'city': 'Bridgeport',
        'state': 'CT'
    }

    def parse(self, response):
      selectors = response.xpath("//div[@class='col-item col-item-inv']")
      for selector in selectors:
        yield from self.parse_car(selector, response.url)

      # next_page = response.xpath("//a[@class='stat-arrow-next']/@href").extract()[0]

      # print("Next Page: ", next_page)
      # if next_page:
      #   next_page_url = f"https://www.irwinzone.com{next_page}"
      #   yield scrapy.Request(
      #       url=next_page_url,
      #       callback=self.parse
      #   )
      # else:
      #   print('No more pages to scrape')

    def parse_car(self, response, current_url):
      item = items.Car()

      get_item_data_from_xpath(response, "//span[@id='MdivYear_0']/text()", item, 'year', 'int')
      get_item_data_from_xpath(response, "//span[@id='MdivMake_0']/text()", item, 'make', 'str')
      get_item_data_from_xpath(response, "//span[@id='MdivModel_0']/text()", item, 'model', 'str')
      get_item_data_from_xpath(response, "//div[@id='MdivTrim_0']/text()", item, 'trim', 'str')
      get_item_data_from_xpath(response, "//div[@id='MDWInvPriceSpan_0']/text()", item, 'price', 'float')
      get_item_data_from_xpath(response, "//div[@id='MdwBoxInvMiles_1']/text()", item, 'price', 'int')
      get_item_data_from_xpath(response, '//li[@class="list-group-item InvEnginetype"]/span/span[@class="dw-p0"]/text()', item, 'engine', 'str')

      title = str(item['year']) + ' ' + str(item['make']) + ' ' + str(item['model']) + str(item['trim'])
      item['title'] = title

      # price = response.xpath("//div[@id='MDWInvPriceSpan_0']/text()").extract()[0].strip()
      # item['price'] = float(price) if price else None

      # vehicle_type = response.xpath("@data-bodystyle").extract()[0].strip()
      # item['vehicle_type'] = vehicle_type if vehicle_type else None

      # item['model_trim'] = item['make'] + ' ' + item['model']

      # mileage = response.xpath("@data-mileage").extract()[0]
      # item['mileage'] = int(mileage) if mileage else None

      # interior_color = response.xpath("@data-intcolor").extract()[0].strip()
      # item['interior_color'] = interior_color if interior_color else None

      # exterior_color = response.xpath("@data-extcolor").extract()[0].strip()
      # item['exterior_color'] = exterior_color if exterior_color else None

      # drivetrain = response.xpath("@data-drivetrain").extract()[0].strip()
      # item['drivetrain'] = drivetrain if drivetrain else None

      # transmission = response.xpath("@data-trans").extract()[0].strip()
      # item['transmission'] = transmission if transmission else None

      # engine = response.xpath("@data-engine").extract()[0].strip()
      # item['engine'] = engine if engine else None

      # vin = response.xpath("@data-vin").extract()[0].strip()
      # item['vin'] = vin if vin else None

      item['dealership_name'] = self.DEALERSHIP_INFO['dealership_name']
      item['dealership_address'] = self.DEALERSHIP_INFO['address']
      item['dealership_zipcode'] = self.DEALERSHIP_INFO['zipcode']
      item['dealership_city'] = self.DEALERSHIP_INFO['city']
      item['dealership_state'] = self.DEALERSHIP_INFO['state']
      item['scraped_url'] = current_url
      item['scraped_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

      yield item
