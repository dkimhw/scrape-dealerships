from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import spiders.stream_auto_outlet_spider as stream_auto_outlet_spider
import spiders.irwin_auto_group_spider as irwin_auto_group_spider
import spiders.ct_auto_spider as ct_auto_spider
import spiders.jm_auto_spider as jm_auto_spider
import spiders.johns_auto_group_spider as johns_auto_group_spider
import spiders.avon_auto_brokers_spider as avon_auto_brokers_spider
import spiders.blasius_boston_spider as blasius_boston_spider
import spiders.newton_auto_sales_spider as newton_auto_sales_spider
import spiders.fafama_auto_sales_spider as fafama_auto_sales_spider
import spiders.direct_auto_spider as direct_auto_spider
import spiders.bostonyan_auto_group_spider as bostonyan_auto_group_spider
import spiders.blasius_boston_spider as blasius_boston_spider
import spiders.hillside_auto_outlet_spider as hillside_auto_outlet_spider
import spiders.queens_auto_mall_spider as queens_auto_mall_spider

def run_spider():
    process = CrawlerProcess(get_project_settings())
    try:
      process.crawl(irwin_auto_group_spider.IrwinAutoGroupSpider)
      process.crawl(stream_auto_outlet_spider.StreamAutoOutletSpider)
      process.crawl(ct_auto_spider.CTAutoSpider)
      process.crawl(jm_auto_spider.JMAutoSpider)
      process.crawl(johns_auto_group_spider.JohnsAutoGroupSpider)
      process.crawl(avon_auto_brokers_spider.AvonAutoBrokersSpider)
      process.crawl(blasius_boston_spider.BlasiusBostonSpider)
      process.crawl(newton_auto_sales_spider.NewtonAutoSalesSpider)
      process.crawl(fafama_auto_sales_spider.FafamaAutoSalesSpider)
      process.crawl(direct_auto_spider.DirectAutoSpider)
      process.crawl(bostonyan_auto_group_spider.BostonyanAutoGroupSpider)
      process.crawl(hillside_auto_outlet_spider.HillsideAutoOutletSpider)
      process.crawl(queens_auto_mall_spider.QueensAutoMallSpider)
      process.start()
    except Exception as e:
      print(e)


if __name__  == '__main__':
  run_spider()
