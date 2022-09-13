from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import spiders.stream_auto_outlet_spider as stream_auto_outlet_spider
import spiders.irwin_auto_group_spider as irwin_auto_group_spider
import spiders.ct_auto_spider as ct_auto_spider
import spiders.jm_auto_spider as jm_auto_spider
import spiders.johns_auto_group_spider as johns_auto_group_spider
import spiders.avon_auto_brokers_spider as avon_auto_brokers_spider


def run_spider():
    process = CrawlerProcess(get_project_settings())
    try:
      # process.crawl(irwin_auto_group_spider.IrwinAutoGroupSpider)
      # process.crawl(stream_auto_outlet_spider.StreamAutoOutletSpider)
      # process.crawl(ct_auto_spider.CTAutoSpider)
      process.crawl(jm_auto_spider.JMAutoSpider)
      process.crawl(johns_auto_group_spider.JohnsAutoGroupSpider)
      process.crawl(avon_auto_brokers_spider.AvonAutoBrokersSpider)
      process.start()
    except Exception as e:
      print(e)


if __name__  == '__main__':
  run_spider()
