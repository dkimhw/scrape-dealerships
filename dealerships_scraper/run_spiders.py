from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import spiders.stream_auto_outlet_spider as stream_auto_outlet_spider
import spiders.irwin_auto_group_spider as irwin_auto_group_spider

def run_spider():
    process = CrawlerProcess(get_project_settings())
    try:
      process.crawl(irwin_auto_group_spider.IrwinAutoGroupSpider)
      process.crawl(stream_auto_outlet_spider.StreamAutoOutletSpider)
      process.start()
    except Exception as e:
      print(e)


if __name__  == '__main__':
  run_spider()
