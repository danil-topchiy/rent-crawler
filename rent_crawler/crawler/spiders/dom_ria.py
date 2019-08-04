import scrapy
import re

from scrapy.exceptions import CloseSpider

from rent_crawler.crawler.items import RentObjectItem
from rent_crawler.core.models import RentObject

ALREADY_SAVED_LINKS_LIMIT = 40


class DomRiaSpider(scrapy.Spider):
    name = 'dom_ria'
    start_url = "https://dom.ria.com/arenda-kvartir/kiev/?page={page}"

    def __init__(self):
        self.page = 1
        # indicator how much links on the page already crawler and saved to db
        self.repeated = 0

    def start_requests(self):
        yield scrapy.Request(url=self.start_url.format(page=self.page), callback=self.parse)

    def parse(self, response):
        rent_objects_links = response.xpath("//section[@data-realtyid]"
                                            "//h3[contains(@class, 'tit')]"
                                            "//a")
        for link in rent_objects_links:
            rent_object_url = response.urljoin(link.xpath('@href').get())

            if RentObject.objects.filter(url=rent_object_url):
                self.repeated += 1
                continue

            if self.repeated >= ALREADY_SAVED_LINKS_LIMIT:
                raise CloseSpider('No new links found')

            yield response.follow(link, callback=self.parse_rent_object, meta={'short_title': link})

        self.page += 1
        yield scrapy.Request(url=self.start_url.format(page=self.page), callback=self.parse)

    def parse_rent_object(self, response):

        def get_normalized_string(xpath_object):
            text = xpath_object.xpath('normalize-space(string(self::node()))').get()
            if text:
                text = text.replace('\xa0', ' ')
            return text

        item = RentObjectItem()
        item['url'] = response.url
        item['short_title'] = get_normalized_string(response.meta.get('short_title'))
        item['city_district_title'] = re.search(r'р‑н. ([а-яА-Я]+)', item['short_title']).group(1)
        item['title'] = get_normalized_string(response.xpath("//div[@class='finalPage']"))
        item['text'] = get_normalized_string(response.xpath("//div[@id='descriptionBlock']"))
        str_price = response.xpath("string(//aside//span[@class='price'])").get()
        item['price'] = int(''.join(re.findall("[0-9]+", str_price)))
        str_rooms = response.xpath("string(//div[@title='Комнат'])").get()
        item['rooms'] = int(re.search("[0-9]+", str_rooms).group())
        yield item
