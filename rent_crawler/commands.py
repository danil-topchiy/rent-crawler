import click
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from rent_crawler.crawler.spiders.dom_ria import DomRiaSpider


@click.command()
def start_crawling():
    crawler_settings = get_project_settings()
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(DomRiaSpider)
    process.start()

