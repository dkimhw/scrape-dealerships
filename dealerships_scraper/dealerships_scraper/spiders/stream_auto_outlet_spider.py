
import scrapy
from ..items import Car
from urllib.parse import urljoin
import re
from scrapy.crawler import CrawlerProcess


class StreamAutoOutletSpider(scrapy.Spider):
    name = "stream_auto_outlet"
    start_urls = [
        'https://www.streamautooutlet.com/inventory?type=used',
    ]

    DEALERSHIP_INFO = {
      'pagination_url': 'https://www.streamautooutlet.com/inventory?type=used&pg=2',
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
        yield scrapy.Request(url, callback=self.parse_car)

      filename = f'links.html'
      with open(filename, 'wb') as f:
          f.write(links)
      self.log(f'Saved file {filename}')

    def parse_car(self, response):
      item = Car()
      vehicle_data1 = response.xpath("//script[contains(text(),'fzDataLayer')]").extract()[1]
      # Parse title
      title = response.xpath("//div[@class='columns vehicle-title']/h1/span/text()").extract()[0]
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
      item['price'] = price if price else None

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
      item['vehicle_mileage'] = mileage
      item['interior_color'] = interior_color
      item['exterior_color'] = exterior_color
      item['drivetrain'] = drivetrain
      item['transmission'] = transmission
      item['engine'] = engine
      item['vin'] = vin


      yield item

      # yield item
    #     for p in products:
    #         url = urljoin(response.url, p)
    #         yield scrapy.Request(url, callback=self.parse_product)

    # def parse_product(self, response):
    #     for info in response.css('div.ph-product-container'):
    #         yield {
    #             'product_name': info.css('h2.ph-product-name::text').extract_first(),
    #             'product_image': info.css('div.ph-product-img-ctn a').xpath('@href').extract(),
    #             'sku': info.css('span.ph-pid').xpath('@prod-sku').extract_first(),
    #             'short_description': info.css('div.ph-product-summary::text').extract_first(),
    #             'price': info.css('h2.ph-product-price > span.price::text').extract_first(),
    #             'long_description': info.css('div#product_tab_1').extract_first(),
    #             'specs': info.css('div#product_tab_2').extract_first(),
    #         }
