
import scrapy
from urllib.parse import urljoin
import re
import time
import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname('dealerships_scraper')))
import items


class StreamAutoOutletSpider(scrapy.Spider):
  name = "stream_auto_outlet"

  # scrapy shell 'https://www.streamautooutlet.com/used-vehicles/?_p=0'
  # https://stackoverflow.com/questions/33247662/how-to-bypass-cloudflare-bot-ddos-protection-in-scrapy
  user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
  start_urls = [
      'https://www.streamautooutlet.com/used-vehicles/?_p=0',
  ]

  DEALERSHIP_INFO = {
    'vehicle_detail_url': 'https://www.streamautooutlet.com/vehicle-details',
    'dealership_name': 'Stream Auto Outlet',
    'address': '324 W Merrick Rd',
    'zipcode': '11580',
    'city': 'Valley Stream',
    'state': 'NY'
  }

  def parse(self, response):
    links = response.xpath("//h4[@class='srp-vehicle-title']/a/@href").extract()
    for link in links:
      url = urljoin(response.url, link)
      time.sleep(1)
      yield scrapy.Request(url, callback=self.parse_car)

    next_page = response.xpath("//a[@class='go-to-page']/@href").extract()

    # Additional layer of logic required to correctly retrieve the next url:
    if next_page:
      if len(next_page) == 2:
        next_page = next_page[0]
      elif len(next_page) > 2:
        next_page = next_page[1]
    else:
      next_page = None
    print("Next Page: ", next_page)
    if next_page:
      next_page_url = f"https://www.streamautooutlet.com/used-vehicles/?_p={next_page}"
      yield scrapy.Request(
          url=next_page_url,
          callback=self.parse
      )
    else:
      print('No more pages to scrape')

  def parse_car(self, response):
    item = items.Car()
    vehicle_data1 = response.xpath("//script[contains(text(),'fzDataLayer')]").extract()[1]
    # Parse title
    title = response.xpath("//div[@class='columns vehicle-title']/h1/span/text()").extract()[0].strip()
    item['title'] = title if title else None

    year = re.search('"year": (.)+,', vehicle_data1 )
    year = int(year.group(0).replace('"year": ', '').replace('"', '').replace(',', ''))
    item['year'] = year if year else None

    make = re.search('"make": (.)+,', vehicle_data1 )
    make = make.group(0).replace('"make": ', '').replace('"', '').replace(',', '')
    item['make'] = make if make else None

    model = re.search('"model": (.)+,', vehicle_data1 )
    model = model.group(0).replace('"model": ', '').replace('"', '').replace(',', '')
    item['model'] = model if model else None

    trim = re.search('"trim": (.)+,', vehicle_data1 )
    trim = trim.group(0).replace('"trim": ', '').replace('"', '').replace(',', '')
    item['trim'] = trim if trim else None

    price = re.search('"sellingprice": (.)+,', vehicle_data1 )
    price = price.group(0).replace('"sellingprice": ', '').replace('"', '').replace(',', '')
    item['price'] = int(price) if price else None

    # Other Vehicle Details
    key_data = response.xpath("//div[has-class('columns', 'show-for-small-only')]/div[@class='vdp-vehicle-details']/ul[@class='no-bullet']/li/span/text()").extract()
    value_data = response.xpath("//div[has-class('columns', 'show-for-small-only')]/div[@class='vdp-vehicle-details']/ul[@class='no-bullet']/li/text()").extract()

    exterior_color = None
    interior_color = None
    transmission = None
    engine = None
    drivetrain = None
    vin = None
    vehicle_type = None
    mileage = None

    for idx, col in enumerate(key_data):
      if 'Ext. Color' in col:
        cleaned_str = value_data[idx].replace('Ext. Color: ', '')
        exterior_color = cleaned_str
      elif 'Int. Color' in col:
        cleaned_str = value_data[idx].replace('Int. Color: ', '')
        interior_color = cleaned_str
      elif 'Transmission' in col:
        cleaned_str = value_data[idx].replace('Transmission: ', '')
        transmission = cleaned_str
      elif 'Mileage' in col:
        cleaned_str = value_data[idx].replace('Mileage: ', '').replace(',', '')
        mileage = cleaned_str
      elif 'Drive Type' in col:
        cleaned_str = value_data[idx].replace('Drive Type: ', '')
        drivetrain = cleaned_str
      elif 'Engine' in col:
        cleaned_str = value_data[idx].replace('Engine: ', '')
        engine = cleaned_str
      elif 'VIN' in col:
        cleaned_str = value_data[idx].split(' ')[1].strip()
        vin = cleaned_str
      elif 'Body Style' in col:
        cleaned_str = value_data[idx].replace('Body Style: ', '')
        vehicle_type = cleaned_str


    item['vehicle_type'] = vehicle_type
    item['model_trim'] = item['make'] + ' ' + item['model']
    item['mileage'] = int(mileage) if mileage else None
    item['interior_color'] = interior_color
    item['exterior_color'] = exterior_color
    item['drivetrain'] = drivetrain
    item['transmission'] = transmission
    item['engine'] = engine
    item['vin'] = vin
    item['dealership_name'] = self.DEALERSHIP_INFO['dealership_name']
    item['dealership_address'] = self.DEALERSHIP_INFO['address']
    item['dealership_zipcode'] = self.DEALERSHIP_INFO['zipcode']
    item['dealership_city'] = self.DEALERSHIP_INFO['city']
    item['dealership_state'] = self.DEALERSHIP_INFO['state']
    item['scraped_url'] = response.url
    item['scraped_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    yield item
