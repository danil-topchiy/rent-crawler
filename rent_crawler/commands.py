import os

import click
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from rent_crawler.crawler.spiders.dom_ria import DomRiaSpider

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, "tests")


@click.command()
def test():
    """Run the tests."""
    import pytest

    rv = pytest.main([TEST_PATH, "--verbose"])
    exit(rv)


@click.command()
def start_crawling():
    crawler_settings = get_project_settings()
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(DomRiaSpider)
    process.start()

