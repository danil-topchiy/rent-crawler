import scrapy
import re

from rent_crawler.crawler.items import RentObjectItem


class DomRiaSpider(scrapy.Spider):
    name = 'dom_ria'
    start_url = "https://dom.ria.com/arenda-kvartir/kiev/?page={page}"

    def __init__(self):
        self.page = 1

    def start_requests(self):
        yield scrapy.Request(url=self.start_url.format(page=self.page), callback=self.parse)

    def parse(self, response):
        rent_objects_links = response.xpath("//section[@data-realtyid]"
                                            "//h3[contains(@class, 'tit')]"
                                            "//a")
        for link in rent_objects_links:
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
        # item['district'] = re.search(r'р‑н. ([а-яА-Я]+)', item['short_title']).group(1)
        item['title'] = get_normalized_string(response.xpath("//div[@class='finalPage']"))
        item['text'] = get_normalized_string(response.xpath("//div[@id='descriptionBlock']"))
        str_price = response.xpath("string(//aside//span[@class='price'])").get()
        item['price'] = int(''.join(re.findall("[0-9]+", str_price)))
        str_rooms = response.xpath("string(//div[@title='Комнат'])").get()
        item['rooms'] = int(re.search("[0-9]+", str_rooms).group())
        yield item
