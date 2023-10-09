import scrapy
import time
import datetime
import os
import re
import sys
sys.path.append(os.path.abspath(os.path.dirname('dealerships_scraper')))
import items
from spiders_utils import get_item_data_from_xpath, get_car_make_model, get_vehicle_type

class DirectAutoSpider(scrapy.Spider):
  name = "direct_auto"
  user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
  start_urls = [
      'https://automecca.com/sale/used-cars-framingham-ma/page-1'
  ]
  pagination_url =  'https://automecca.com/sale/used-cars-framingham-ma/page-1'

  DEALERSHIP_INFO = {
    'dealership_name': 'Direct Auto Mecca',
    'address': '154 Waverly Street',
    'zipcode': '01760',
    'city': 'Natick',
    'state': 'MA'
  }

  # int(re.search('page-([0-9])+', 'https://automecca.com/sale/used-cars-framingham-ma/page-1')[0].replace('page-', ''))
  # re.sub('page-([0-9])+', f'page={curr_page + 1}', 'https://automecca.com/sale/used-cars-framingham-ma/page-1')

  def parse(self, response):
    links = response.xpath("//div[@class='veh-title-bar group']/h2/a/@href").extract()
    if len(links) == 0:
      return

    vehicle_trims = response.xpath("//div[@class='veh-title-bar group']/h2/a/span[@class='title-item trim']/text()").extract()
    for idx in range(len(links)):
      time.sleep(1)
      url = f'https://automecca.com{links[idx]}'
      trim = vehicle_trims[idx]
      yield scrapy.Request(url, callback=self.parse_car, cb_kwargs=dict(trim=trim))

    curr_page = int(re.search('page-([0-9])+', self.pagination_url)[0].replace('page-', '')) if re.search('page-([0-9])+', self.pagination_url) else 1
    self.pagination_url = re.sub('page-([0-9])+', f'page-{curr_page + 1}', self.pagination_url)
    yield scrapy.Request(
      url=self.pagination_url,
      callback=self.parse
    )

  def parse_car(self, response, trim):
    item = items.Car()

    get_item_data_from_xpath(response, "//div[@class='simpwebchat_inv_item']/@data-year", item, 'year', 'int', 0)
    get_item_data_from_xpath(response, "//div[@class='simpwebchat_inv_item']/@data-make", item, 'make', 'str', 0)
    get_item_data_from_xpath(response, "//div[@class='simpwebchat_inv_item']/@data-model", item, 'model', 'str', 0)
    item['trim'] = trim.strip()
    item['title'] = str(item['year']) + ' ' + str(item['make']) + ' ' + str(item['model']) + ' ' + str(item['trim']) if item['trim'] != None else ''
    item['model_trim'] = str(item['model']) + ' ' + str(item['trim']) if item['trim'] != None else ''

    get_item_data_from_xpath(response, "//div[@class='left-half-col']/dl/dd[preceding-sibling::dt/text()[contains(., 'Mileage:')]]/text()", item, 'mileage', 'int')
    get_item_data_from_xpath(response, ".//div[@class='simpwebchat_inv_item']/@data-price", item, 'price', 'int')

    get_item_data_from_xpath(response, "//div[@class='left-half-col']/dl/dd[preceding-sibling::dt/text()[contains(., 'Body:')]]/text()", item, 'vehicle_type', 'str')
    get_item_data_from_xpath(response, "//div[@class='right-half-col']/dl/dd[preceding-sibling::dt/text()[contains(., 'Transmission:')]]/text()", item, 'transmission', 'str')
    get_item_data_from_xpath(response, ".//div[@class='simpwebchat_inv_item']/@data-vin", item, 'vin', 'str')
    get_item_data_from_xpath(response, "//div[@class='right-half-col']/dl/dd[preceding-sibling::dt/text()[contains(., 'Engine:')]]/text()", item, 'engine', 'str')
    get_item_data_from_xpath(response, "//div[@class='left-half-col']/dl/dd[preceding-sibling::dt/text()[contains(., 'Interior:')]]/text()", item, 'interior_color', 'str')
    get_item_data_from_xpath(response, "//div[@class='left-half-col']/dl/dd[preceding-sibling::dt/text()[contains(., 'Exterior:')]]/text()", item, 'exterior_color', 'str')
    get_item_data_from_xpath(response, "//div[@class='left-half-col']/dl/dd[preceding-sibling::dt/text()[contains(., 'Drivetrain:')]]/text()", item, 'drivetrain', 'str')

    # response.xpath("//div[@class='left-half-col']/dl/dd[preceding-sibling::dt/text()[contains(., 'Drivetrain:')]]/text()").extract()
    # response.xpath("//div[@class='left-half-col']/dl/dd/text()").extract()

    item['dealership_name'] = self.DEALERSHIP_INFO['dealership_name']
    item['dealership_address'] = self.DEALERSHIP_INFO['address']
    item['dealership_zipcode'] = self.DEALERSHIP_INFO['zipcode']
    item['dealership_city'] = self.DEALERSHIP_INFO['city']
    item['dealership_state'] = self.DEALERSHIP_INFO['state']
    item['scraped_url'] = response.url
    item['scraped_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    yield item
