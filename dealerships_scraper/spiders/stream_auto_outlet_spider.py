
import scrapy
from urllib.parse import urljoin
import re
# import time
import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname('dealerships_scraper')))
from scrapy_selenium import SeleniumRequest
import items

class StreamAutoOutletSpider(scrapy.Spider):
  name = "stream_auto_outlet"

  def start_requests(self):
    url = 'https://www.streamautooutlet.com/used-vehicles/'
    print(url)

    yield SeleniumRequest(url=url, callback=self.parse)

  def parse(self, response):
    print(response.request.meta['driver'].title)
